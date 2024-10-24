import ollama
from langchain_ollama import OllamaEmbeddings
import pymongo
import urllib.parse
from llama_index.core import VectorStoreIndex
from langchain_nomic.embeddings import NomicEmbeddings
import requests



print('\n')
print('\n')

initial_question = input("ask a Adobe Campaign question?     \n")

print('\n')
print('\n')

#the main function
def sendQuery(query):
 #my credientials for mongodb atlas
 username = urllib.parse.quote_plus('admin')
 password = urllib.parse.quote_plus('Thenorthface1')
#The URL for my mongodb database
 url= f"mongodb+srv://{username}:{password}@cluster0.yy5c5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#creating the database session
 myclient = pymongo.MongoClient(url)
#Embedding the question
 res = ollama.embeddings(
  prompt = query,
  model = 'nomic-embed-text'
 )
# creating the pipeline or "query"
 pipeline = [{
  "$vectorSearch": {
    "exact": False,
    "index": "vector_index",
    "limit": 3,
    "numCandidates": 4400,
    "path": "embedding",
    "queryVector": res["embedding"]
   }
  },      
    {
     "$project": {
       "_id": 0, 
       "plot": 1, 
       "title": 1,
       "page_content":1,
       "score": {
         '$meta': 'vectorSearchScore'
        }
       }
    }  
 ]
#  pipeline = [{
#     "$search": {
#       "index": "default",
#       "text": {
#         "query": initial_question,
#         "path": {
#           "wildcard": "*"
#         }
#       }
#     }
#   },      
#     {
#      "$project": {
#        "_id": 0, 
#        "title": 1,
#        "page_content":1,
#        "score": {
#          '$meta': 'vectorSearchScore'
#         }
#        }
#     },
#     {
#       "$limit":5
#     }
# ]
 result = myclient['RAG_AI_APPLICATION']['ACC_DOC'].aggregate(pipeline=pipeline)

 text_arr=''
 response_arr =[]
 counter = 0

 for i in result:
  response_arr.append(i)
  text_arr = text_arr + str(i['page_content'])

 res = str(response_arr)
 print("This is a paragraph from the adobe documentation that may answer your question while the LLM learns relevant documentation data: "+ '\n' + text_arr)



 def chat_funct(response_arr, query):
  context_statement = f'this is context for the prompt: {response_arr}, can you answer this question? {query}'
  stream = ollama.chat(
   model='llama3.1',
   messages=[{'role':'user','content':context_statement}],
   stream=True
  )
  print('\n')
  print('\n')
  print(query )
  print('\n')
  print('\n')

  string =''
  print("Loading........")
  for chunk in stream:
    string += chunk["message"]["content"]
  return string
 
 
 print(chat_funct(response_arr=res,query=initial_question))


def chat_response(string, input):
  print(string)

  stream = ollama.chat(
    model='llama3.1',
    messages=[{'role':'user','prompt': input}],
    stream=True
  )
  print('\n')
  print('\n')
  newstring =''
  print("Loading........")
  for chunk in stream:
    
    newstring += chunk["message"]["content"]
  print(str(newstring)  )
  return str(newstring)


print('\n')
print('\n') 
try:
  response = sendQuery(initial_question)
  print(str(response))
except:
  print("error occured")
finally:
  print("DONE")
