<div align = "center">

<h1>BOOKIPEDIA-AI</h1>
<h3>RAG, OCR, TTS and More</h3>

<em>Part of the (Bookipedia App) a graduation project at CSED MU.</em>

[![Frontend](https://img.shields.io/badge/frontend-02569B?logo=flutter&logoColor=white)](https://github.com/nadahossamismail/Bookipedia) [![Backend](https://img.shields.io/badge/backend-339933?logo=nodedotjs&logoColor=white)](https://github.com/mhmadalaa/bookipedia) [![License: GPL-3.0](https://img.shields.io/badge/license-GPLv3.0-orange.svg)](https://www.gnu.org/licenses/gpl-3.0) [![CodeFactor](https://www.codefactor.io/repository/github/yousefmrashad/bookipedia/badge/main)](https://www.codefactor.io/repository/github/yousefmrashad/bookipedia/overview/main) 



</div>


##  Overview

Bookipedia is an online library with an AI powered reading assistant, revolutionizing the digital reading experience by providing users with insights and answers to their questions about their books and documents, summaries and even web research, all through a natural-language chat. In addition, users can upload scanned documents to convert them to readable PDFs and use text to speech to set back and listen to their favourite books. 

---

##  Features

### Core Technologies
- **State-of-the-Art OCR Models**
  - Lightning fast and accurate conversion of scanned documents into selectable, readable PDFs.

- **Vector Indexing**
  - Creation of vector indices using embeddings generated by SoTA Sentence-Transformer models.
  - Integration with Weaviate vector database for efficient, accurate data retrieval.

- **Retrieval-Augmented Generation (RAG)**
  - Utilization of advanced RAG techniques to achieve high groundedness, and context and answer relevance.
  - Utilization of GPT and Gemini LLMs for generating insights, and accurate and reliable answers.
  - Capable of retrieving information both from the book content and through web research.

### Functional Features
- **Document Conversion**
  - Upload scanned documents and convert them into readable PDFs.

- **Question & Answer**
  - Provide insights and answer user queries about book content using advanced RAG techniques.
  - Perform web research to provide comprehensive answers.

- **Summarization**
  - Generate concise summaries of book pages or entire documents.

- **Text-to-Speech**
  - Read back text from books and documents, offering a hands-free reading experience.

---

##  Modules

<details closed><summary>preprocessing</summary>

| File                                           | Summary                                                                                                                                                                                                                                                                                                                             |
| ---                                            | ---                                                                                                                                                                                                                                                                                                                                 |
| [embedding.py](preprocessing/embedding.py)     | Interfaces for AnglE and Hugging Face sentence transformers.Interfaces support embedding documents and queries, enabling efficient text representation for downstream tasks.                                                                   |
| [ocr.py](preprocessing/ocr.py)                 | OCR performs optical character recognition on a PDF document, extracting text and converting it into an editable format. It employs image filtering, skew correction, and OCR techniques to enhance accuracy. The resulting text is exported as an XML file and converted into a PDF with HOCR annotations for easy text retrieval. |
| [document.py](preprocessing/document.py)       | Document processing orchestrates the transformation of raw documents into structured data. It leverages OCR for scanned documents and converts to markdown text-based ones, splits them into chunks, generates embeddings, and stores them in the vector database for efficient retrieval.                                                                                                                                                                                                       |

</details>

<details closed><summary>rag</summary>

| File                                               | Summary                                                                                                                                                                                                                                                                                                                                                                                              |
| ---                                                | ---                                                                                                                                                                                                                                                                                                                                                                                                  |
| [web_researcher.py](rag/web_researcher.py)         | WebResearchRetriever facilitates web research by utilizing DuckDuckGos Search API to retrieve relevant webpages. It employs an LLM to generate search queries, searches for URLs, and indexes new webpages into a vector store. The retriever then searches for relevant document splits within the vector store, ensuring unique and pertinent results.                                                |
| [rag_pipeline.py](rag/rag_pipeline.py)             | RAGPipeline orchestrates the retrieval and summarization of information from a Weaviate vector database and the web. It generates retrieval queries, combines context from multiple sources, and produces answers to user questions using a large language model. The pipeline also updates the chat summary based on user interactions, ensuring natural conversation flow, and implements page summarization functionality. |
| [weaviate_retriever.py](rag/weaviate_retriever.py) | Weaviate Retriever facilitates hybrid searches, combining both semantic and keyword searching by leveraging a vector store to retrieve relevant documents based on a given query. It offers advanced features like auto-merging and re-ranking to enhance search accuracy.                                                                                                                                                                      |
| [web_weaviate.py](rag/web_weaviate.py)             | Integrates with Weaviate vector store, enabling text embedding and similarity search for web retrieval tasks.                                                                                                                                                                                                                                                                                                                |                                                                                                                                                                                                                                                              |

</details>

<details closed><summary>utils</summary>

| File                                   | Summary                                                                                                                                                                                                                                                                                    |
| ---                                    | ---                                                                                                                                                                                                                                                                                        |
| [font.py](utils/font.py)               | Font manipulation empowers the hOCR module to encode text, estimate its width, and register fonts within a PDF document. It provides a glyphless font for placeholder text and a Courier font for standard text rendering.                                                                        |
| [hocr.py](utils/hocr.py)               | This code transforms documents from the hOCR format into PDF files, preserving the original texts position and orientation. It also provides debugging options to visualize the bounding boxes and baselines of text elements, aiding in the verification of the transformations accuracy. |
| [init.py](utils/init.py)               | Centralizes imports for utility modules, facilitating code organization and reusability within the Bookipedia repository.                                                                                                                                                                  |
| [config.py](utils/config.py)           | Configures essential settings and constants for the Bookipedia repository. It establishes root paths, imports necessary modules, defines constants, and sets up models and URLs for various functionalities, including OCR, TTS, document loading, embeddings, the LLM and backend API calls.                    |
| [db_config.py](utils/db_config.py)     | Configures and manages the Weaviate database connection, ensuring its existence and proper schema.                                                                                                                                                                                         |
| [functions.py](utils/functions.py)     | Provides utility functions for OCR, document loading, retrieval filtering, and text processing to support document processing and retrieval. Key features include image value scaling, token counting, filtering by IDs and page numbers, merging text chunks with overlap handling, and calculating the percentage of document area covered by images.                                                               |                                                                                                         |

</details>


<details closed><summary>api</summary>

| File                                   | Summary                                                                                                                                                                                                                                                                                                                                                |
| ---                                    | ---                                                                                                                                                                                                                                                                                                                                                    |
| [api.py](api/api.py)                   | This API serves as the core inference engine for the Bookipedia application, providing AI-powered document processing, chat response generation, text-to-speech synthesis, and page summarization. It integrates seamlessly with the application's architecture, ensuring efficient and scalable AI inference. The API supports background tasks for document and chat processing, enabling asynchronous operations and enhanced performance.                                                                                                                            |
| [schemas.py](api/schemas.py)           | This file establishes the structure of request bodies for the API, ensuring consistent and well-formed data input. It defines schemas for chat parameters and text-to-speech requests, facilitating seamless communication between the API and its clients.                                                                                            |                                                                                                                                                                                                                                            |

</details>


---

##  Getting Started

**System Requirements:**

* **Operating System**: Only 64-bit Linux systems are currently supported.
* **Python**: `version 3.10.x` (It is recommended to create a clean environment for the server)
* **CUDA**: A functioning CUDA and cuDNN environment with a minimum CUDA version of `11.x`.

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the bookipedia repository:
>
> ```console
> $ git clone https://github.com/yousefmrashad/bookipedia
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd bookipedia
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run the server using the command below:
> ```console
> $ python api/api.py
> ```
> 
---

## Models and Frameworks
### AI Models
- [db_mobilenet_v3_large](https://mindee.github.io/doctr/using_doctr/using_models.html#:~:text=PyTorch-,db_mobilenet_v3_large,-(1024%2C%201024%2C%203)) for text detection.
- [crnn_mobilenet_v3_large](https://mindee.github.io/doctr/using_doctr/using_models.html#:~:text=PyTorch-,crnn_mobilenet_v3_large,-(32%2C%20128%2C%203)) for text recognition.
- [gte-large-en-v1.5](https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5) sentence transformer.
- [jina-reranker-v1-turbo-en](https://huggingface.co/jinaai/jina-reranker-v1-turbo-en) reranker.
- [gpt-3.5-turbo-0125](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4#:~:text=TRAINING%20DATA-,gpt%2D3.5%2Dturbo%2D0125,-New%20Updated%20GPT) large language model.
- [VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech](https://github.com/jaywalnut310/vits)

### Tools and Frameworks
- [FastAPI](https://fastapi.tiangolo.com/)
- [Weaviate Vector Database](https://weaviate.io/)
- [LangChain](https://www.langchain.com/)
- [docTR](https://github.com/mindee/doctr)
- [Piper](https://github.com/rhasspy/piper)

---

##  License
This project is protected under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0) License, unless otherwise specified. Certain files may have separate licenses, which can be found in the [LICENSES](https://github.com/yousefmrashad/bookipedia/blob/main/LICENSES) folder.


---

##  Team
This part of the project was made possible with the equal contributions of:

- [Yousef Rashad](https://github.com/yousefmrashad)
- [Mohamed Hazem](https://github.com/mohamed-hazem)
- [Abdelhakiem Osama](https://github.com/Abdelhakiem) 

And our front-end and back-end teams!

---

[**Return**](#overview)
