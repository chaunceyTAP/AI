import os
# from dotenv import load_dotenv
from langchain_community.document_loaders.mongodb import MongodbLoader
# import nest_asyncio
import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import pymongo
import ollama
import csv
import nomic
from uuid import uuid4
from langchain_core.documents import Document
from nomic import embed
import motor
# nest_asyncio.apply()
# load_dotenv()

## CONNECTION TO MONGODB
username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('Thenorthface1')
url= f"mongodb+srv://{username}:{password}@cluster0.yy5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(url)
myclient = pymongo.MongoClient(url)



loader = MongodbLoader(
    connection_string=url,
    db_name='RAG_AI_APPLICATION',
    collection_name='store',
    filter_criteria={},
    # field_names=["title", "plot"]
)
docs = loader.load()

print(len(docs))



DB_NAME = myclient["RAG_AI_APPLICATION"]
COLLECTION_NAME = DB_NAME["store"]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"
print(DB_NAME.list_collection_names())
# MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]


nomic.login('nk-w4VCdJcsu1jShMyYKZRiw_aPhi7oowyx6fLjnJWJKuM')

embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=256)

# QUERY MONGO DB


document_1 = Document(
    page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

documents = [
    document_1,
    document_2,
]
uuids = [str(uuid4()) for _ in range(len(documents))]
print(documents, uuids)

vector_store = MongoDBAtlasVectorSearch.from_documents(
  documents=documents,
  embedding=embeddings,
  collection=COLLECTION_NAME,
  index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME
)
print('Properly added vectors!!!!!!!!!')


