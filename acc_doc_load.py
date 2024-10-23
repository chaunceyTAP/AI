import os
from langchain_community.document_loaders.mongodb import MongodbLoader
import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.llms import OpenAI
# from langchain_community.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
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
import pandas as pd
import json
## CONNECTION TO MONGODB
username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('Thenorthface1')
url= f"mongodb+srv://{username}:{password}@cluster0.yy5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
myclient = pymongo.MongoClient(url)

loader = MongodbLoader(
    connection_string=url,
    db_name='RAG_AI_APPLICATION',
    collection_name='ACC_DOCS',
    filter_criteria={},
    # field_names=["title", "plot"]
)
docs = loader.load()


DB_NAME = myclient["RAG_AI_APPLICATION"]
COLLECTION_NAME = DB_NAME["STORE2"]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"
# print(DB_NAME.list_collection_names())

# nomic.login('nk-0Rg_LYCsGGQAMrcjTcIAPvGxHnmXfdNPZpBuaPhBIT0')
print('logged in to nomic')
# embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", dimensionality=768)

# embedding = ollama.embeddings(
#  model='nomic-embed-text',
#  promt=''
# )

print('nomic embeddings set')
#function that reads the josn files
base_dir ='./interim-data/'
docs_to_be_loaded = []

for file in os.listdir(base_dir):
 print(file)

 json_path = os.path.join(base_dir, file)
 f =open('interim-data/'+file, encoding="utf8")
 json_data = json.load(f)
 # json_data = pd.read_json(json_path, lines=True)
 uuid = json_data['guid']
 title =json_data['title']
 full_text = json_data['fullText']

 blah = ollama.embeddings(model='nomic-embed-text',prompt=full_text)
 embedding = blah['embedding']
 doc = Document(
  uuid = uuid,
  page_content=str(full_text),
  title = title,
  embedding = embedding,
  metadata={
   "source":"ADOBE CAMPAIGN CLASSIC DOCUMENTATION",
   "guid":uuid,
   "title":title
   }
 )


vector_store = MongoDBAtlasVectorSearch.from_documents(
  
  documents=docs_to_be_loaded,
  # embedding=embeddings,
  collection=COLLECTION_NAME,
  index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME

)
print('Properly added vectors!!!!!!!!!')


