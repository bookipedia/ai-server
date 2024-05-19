# Utils
from root_config import *
from utils.init import *
# ================================================== #

import logging
import re
from typing import List, Optional

from langchain_community.document_loaders.async_html import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.language_models import BaseLLM
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BasePromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from langchain.chains.llm import LLMChain
from langchain.chains.prompt_selector import ConditionalPromptSelector

logger = logging.getLogger(__name__)


class SearchQueries(BaseModel):
    """Search queries to research for the user's goal."""

    queries: List[str] = Field(
        ..., description="List of search queries to look up on DuckDuckGo"
    )


DEFAULT_LLAMA_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""<<SYS>> \n You are an assistant tasked with improving DuckDuckGo search \
results. \n <</SYS>> \n\n [INST] Generate THREE DuckDuckGo search queries that \
are similar to this question. The output should be a numbered list of questions \
and each should have a question mark at the end: \n\n {question} [/INST]""",
)

DEFAULT_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an assistant tasked with improving DuckDuckGo search \
results. Generate THREE DuckDuckGo search queries that are similar to \
this question. The output should be a numbered list of questions and each \
should have a question mark at the end: {question}""",
)


class QuestionListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of numbered questions."""

    def parse(self, text: str) -> List[str]:
        lines = re.findall(r"\d+\..*?(?:\n|$)", text)
        return lines


class WebResearchRetriever(BaseRetriever):
    """`DuckDuckGo Search API` retriever."""

    # Inputs
    vectorstore: VectorStore = Field(
        ..., description="Vector store for storing web pages"
    )
    llm_chain: LLMChain
    search: DuckDuckGoSearchAPIWrapper = Field(..., description="DuckDuckGo Search API Wrapper")
    num_search_results: int = Field(1, description="Number of pages per DuckDuckGo search")
    text_splitter: TextSplitter = Field(
        RecursiveCharacterTextSplitter(chunk_size=480, chunk_overlap=32),
        description="Text splitter for splitting web pages into chunks",
    )
    url_database: List[str] = Field(
        default_factory=list, description="List of processed URLs"
    )

    @classmethod
    def from_llm(
        cls,
        vectorstore: VectorStore,
        llm: BaseLLM,
        search: DuckDuckGoSearchAPIWrapper,
        prompt: Optional[BasePromptTemplate] = None,
        num_search_results: int = 1,
        text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        ),
    ) -> "WebResearchRetriever":
        """Initialize from llm using default template.

        Args:
            vectorstore: Vector store for storing web pages
            llm: llm for search question generation
            search: DuckDuckGoSearchAPIWrapper
            prompt: prompt to generating search questions
            num_search_results: Number of pages per DuckDuckGo search
            text_splitter: Text splitter for splitting web pages into chunks

        Returns:
            WebResearchRetriever
        """

        if not prompt:
            QUESTION_PROMPT_SELECTOR = ConditionalPromptSelector(
                default_prompt=DEFAULT_SEARCH_PROMPT,
                conditionals=[
                    (lambda llm: isinstance(llm, LlamaCpp), DEFAULT_LLAMA_SEARCH_PROMPT)
                ],
            )
            prompt = QUESTION_PROMPT_SELECTOR.get_prompt(llm)

        # Use chat model prompt
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            output_parser=QuestionListOutputParser(),
        )

        return cls(
            vectorstore=vectorstore,
            llm_chain=llm_chain,
            search=search,
            num_search_results=num_search_results,
            text_splitter=text_splitter,
        )

    def clean_search_query(self, query: str) -> str:
        # Some search tools (e.g., DuckDuckGo) will
        # fail to return results if query has a
        # leading digit: 1. "LangCh..."
        # Check if the first character is a digit
        if query[0].isdigit():
            # Find the position of the first quote
            first_quote_pos = query.find('"')
            if first_quote_pos != -1:
                # Extract the part of the string after the quote
                query = query[first_quote_pos + 1 :]
                # Remove the trailing quote if present
                if query.endswith('"'):
                    query = query[:-1]
        return query.strip()

    def search_tool(self, query: str, num_search_results: int = 1) -> List[dict]:
        """Returns num_search_results pages per DuckDuckGo search."""
        query_clean = self.clean_search_query(query)
        result = self.search.results(query_clean, num_search_results)
        return result

    def _get_relevant_documents(
        self,
        query: str,
        k: int = 2,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """Search DuckDuckGo for documents related to the query input.

        Args:
            query: user query

        Returns:
            Relevant documents from all various urls.
        """

        # Get search questions
        logger.info("Generating questions for DuckDuckGo Search ...")
        result = self.llm_chain.invoke({"question": query})
        logger.info(f"Questions for DuckDuckGo Search (raw): {result}")
        questions = result["text"]
        logger.info(f"Questions for DuckDuckGo Search: {questions}")

        # Get urls
        logger.info("Searching for relevant urls...")
        urls_to_look = []
        for query in questions:
            # DuckDuckGo search
            search_results = self.search_tool(query, self.num_search_results)
            logger.info("Searching for relevant urls...")
            logger.info(f"Search results: {search_results}")
            for res in search_results:
                if res.get("link", None):
                    urls_to_look.append(res["link"])

        # Relevant urls
        urls = set(urls_to_look)

        # Check for any new urls that we have not processed
        new_urls = list(urls.difference(self.url_database))

        logger.info(f"New URLs to load: {new_urls}")
        # Load, split, and add new urls to vectorstore
        if new_urls:
            loader = AsyncHtmlLoader(new_urls, ignore_load_errors=True)
            html2text = Html2TextTransformer()
            logger.info("Indexing new urls...")
            docs = loader.load()
            docs = list(html2text.transform_documents(docs))
            docs = self.text_splitter.split_documents(docs)
            self.vectorstore.add_documents(docs)
            self.url_database.extend(new_urls)

        # Search for relevant splits
        logger.info("Grabbing most relevant splits from urls...")
        docs = []
        for query in questions:
            docs.extend(self.vectorstore.similarity_search(query, k=k))

        # Get unique docs
        unique_documents_dict = {
            (doc.page_content, tuple(sorted(doc.metadata.items()))): doc for doc in docs
        }
        unique_documents = list(unique_documents_dict.values())
        # self.vectorstore.delete()
        return unique_documents

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
    ) -> List[Document]:
        raise NotImplementedError
