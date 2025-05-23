# Using PyTorch
import os
os.environ["USE_TORCH"] = "1"
# --------------------------------------------------------------------- #

# -- Modules -- #

# Basics
import torch
import re, json, math, requests, asyncio
from collections import Counter
import math
import logging

# Image Preprocessing
import numpy as np
import cv2 as cv

# HOCR
import PIL.Image
from pikepdf import Pdf

# Document Loading
import fitz
import tiktoken
from pdf4llm import to_markdown
from langchain_community.document_loaders.pdf import PyPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Embeddings
from sentence_transformers import SentenceTransformer

# Weaviate Class
import weaviate
import weaviate.classes as wvc
from weaviate.collections.classes.grpc import Sort
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_community.vectorstores.utils import maximal_marginal_relevance
from sentence_transformers import CrossEncoder
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

# LLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Type Hinting
from typing import Annotated, AsyncIterator
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from weaviate import WeaviateClient
from weaviate.collections.classes.internal import QueryReturn, Object, ReturnProperties

# Secret Keys
from dotenv import load_dotenv
if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPEN_AI_KEY"):
    load_dotenv() 
# --------------------------------------------------------------------- #

# -- Constants -- #
ROOT = os.path.dirname(os.path.dirname(__file__))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
# LLM_MODEL_NAME = "gpt-4.1"
LLM_MODEL_NAME = "models/gemini-2.0-flash"


# OCR
DETECTION_MODEL = "db_mobilenet_v3_large"
RECOGNITION_MODEL = "crnn_mobilenet_v3_large"

# Document Load
CHUNK_SIZE = 128
CHUNK_OVERLAP = 32
MD_SEPARATORS = [
                # First, try to split along Markdown headings (starting with level 2)
                "\n#{1,6} ",
                # Note the alternative syntax for headings (below) is not handled here
                # Heading level 2
                # ---------------
                # End of code block
                "```\n",
                # Horizontal lines
                "\n\\*\\*\\*+\n",
                "\n---+\n",
                "\n___+\n",
                # Note that this splitter doesn't handle horizontal lines defined
                # by *three or more* of ***, ---, or ___, but this is not handled
                "\n\n",
                r"(?<=\w{2}\.\s)",
                "\n",
                " ",
                "",
            ]
SEPARATORS = [r"(?<=\w{2}\.\s)", "\n"]
ENCODING_NAME = "cl100k_base"

# Auto Merging
L1 = 4
L2 = 16

# Retrieving Filters
SORT = Sort.by_property(name="index", ascending=True)

# Embedding Model
EMBEDDING_MODEL_NAME = "jinaai/jina-embeddings-v3"
RETRIEVAL_PROMPT = "Represent this sentence for searching relevant passages: " 

# Re-ranker Model
# RERANKER_MODEL_NAME = "mixedbread-ai/mxbai-rerank-large-v1"
RERANKER_MODEL_NAME = "jinaai/jina-reranker-v2-base-multilingual"

# Database Name
DB_NAME = "bookipedia"

# TTS Model Paths
PIPER_MODEL_PATH = os.path.join(ROOT, "models/en_US-amy-medium.onnx")
PIPER_CONFIG_PATH = PIPER_MODEL_PATH + ".json"

# Back-End URLs
BACKEND_URL = "https://bookipedia-backend.onrender.com/ai-api/"
# FILE_URL = BACKEND_URL + "file/"
CHAT_SUMMARY_URL = BACKEND_URL + "chat-summary/"
POST_HOCR_URL = BACKEND_URL + "ocr-file/"
ACKNOWLEDGE_URL = BACKEND_URL + "ai-applied/"

# RAG
SUMMARY_TOKEN_LIMIT = 8064
FETCHING_LIMIT = 1024
# --------------------------------------------------------------------- #