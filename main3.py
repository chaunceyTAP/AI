import ollama
from langchain_ollama import OllamaEmbeddings
import pymongo
import urllib.parse
from llama_index.core import VectorStoreIndex
from langchain_nomic.embeddings import NomicEmbeddings

# import faiss

def sendQuery(query):
 username = urllib.parse.quote_plus('admin')
 password = urllib.parse.quote_plus('Thenorthface1')
 url= f"mongodb+srv://{username}:{password}@cluster0.yy5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
 myclient = pymongo.MongoClient(url)

 embeddings = OllamaEmbeddings(model="llama3")
#  embedding = NomicEmbeddings()

 DB_NAME = myclient["RAG_AI_APPLICATION"]


 ACC_DOCS = DB_NAME.get_collection('ACC_DOCS')

 res = ollama.embeddings(
  prompt = query,
  model = 'nomic-embed-text'
 )
#  print(res)

 pipeline = [{

  
  "$vectorSearch": {
    "exact": False,
    "index": "vector_index",
    "limit": 10,
    "numCandidates": 800,
    "path": "embedding",
    "queryVector": res["embedding"]
   }
  },      
    {
     "$project": {
       "_id": 1, 
       "plot": 1, 
       "title": 1, 
       "embedding":1,
       "score": {
         '$meta': 'vectorSearchScore'
        },
        
       }
    }
  
 ]
 result = myclient['RAG_AI_APPLICATION']['ACC_DOCS'].aggregate(pipeline=pipeline)



 # print("printed list :" + str(list(result)))
 for i in result[0]:
  print(i)
  print('\n')

sendQuery("")
