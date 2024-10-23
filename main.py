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
#  pipeline = [{
#   "$vectorSearch": {
#     "exact": False,
#     "index": "vector_index",
#     "limit": 3,
#     "numCandidates": 4400,
#     "path": "embedding",
#     "queryVector": res["embedding"]
#    }
#   },      
#     {
#      "$project": {
#        "_id": 0, 
#        "plot": 1, 
#        "title": 1,
#        "page_content":1,
#        "score": {
#          '$meta': 'vectorSearchScore'
#         }
#        }
#     }  
#  ]
 pipeline = [{
    "$search": {
      "index": "default",
      "text": {
        "query": initial_question,
        "path": {
          "wildcard": "*"
        }
      }
    }
  },      
    {
     "$project": {
       "_id": 0, 
       "title": 1,
       "page_content":1,
       "score": {
         '$meta': 'vectorSearchScore'
        }
       }
    },
    {
      "$limit":3
    }
]
 result = myclient['RAG_AI_APPLICATION']['ACC_DOC'].aggregate(pipeline=pipeline)

#  print("printed list :" + str(list(result)))
 text_arr=''
 response_arr =[]
 counter = 0
 for i in result:
  # print(str(i), counter)
  response_arr.append(i)
  text_arr = text_arr + str(i['page_content'])
  # print(str(i['page_content']))
  # print(len(response_arr))

 res = str(response_arr)
 print("This is a paragraph from the adobe documentation that may answer your question while the LLM learns relevant documentation data: "+ '\n' + text_arr)



 def chat_funct(response_arr, query):
  # query = "can you summarize the main points of the following message? please go into detail about any topic you deem is relevant!"
  context_statement = f'this is context for the prompt: {response_arr}, can you answer this question? {query}'
  stream = ollama.chat(
   model='llama3.1',
   messages=[{'role':'user','content':context_statement}],
  #  context=response_arr,
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
  # print(string)
  return string
 
 
 print(chat_funct(response_arr=res,query=initial_question))


def chat_response(string, input):
  print(string)
  # print("ask the ui a question")
  # input = input("ask the ui a question")
  stream = ollama.chat(
    model='llama3.1',
    messages=[{'role':'user','prompt': input}],
  #  context=response_arr,
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
  # input = input("ask the ui a question?    \n")

  # print('\n')
  # print('\n')
  # stream = ollama.chat(
  #   model='llama3.1',
  #   messages=[{'role':'user','prompt': input}],
  # #  context=response_arr,
  #   stream=True
  # )
  # print('\n')
  # print('\n')
  # newstring =''
  # print("Loading........")
  # for chunk in stream:
    
  #   newstring += chunk["message"]["content"]
  # print(str(newstring)  )
  # return str(newstring)
  # print(input)
  # ollama_response = 
  # chat_response( response, input=input)


# # # def continued_chat(happy):
# # #   stream = ollama.chat(
# # #     model='llama3.1',
# # #     messages=[{'role':'user','prompt': f" {happy}"}],
# # #   #  context=response_arr,
# # #     stream=True
# # #   )
# # #   print('\n')
# # #   print('\n')
# # #   newstring =''
# # #   print("Loading........")
# # #   for chunk in stream:
# # #     newstring += chunk["message"]["content"]

# # #   print(newstring)  
# # #   return newstring

# # # happy = input("are you happy with this info?? reply with 'Y' or 'N'    \n")
# # # if happy.lower() == "n":
  
# # #   next_question = input("ask another question!    \n")
# # #   while next_question == "n":
# # #     continued_chat(happy=happy)
    





# # # 20.42.2.0/23
# # # 20.42.4.0/26
# # # 20.42.64.0/28
# # # 20.49.111.0/29
# # # 40.71.14.32/28
# # # 40.78.229.96/28
# # # 20.41.2.0/23
# # # 20.41.4.0/26
# # # 20.44.17.80/28
# # # 20.49.102.16/29
# # # 40.70.148.160/28
# # # 52.167.107.224/28
# # # 20.98.198.224/29
# # # 20.119.28.57/32
# # # 20.232.89.104/29
# # # 20.98.195.172/32
# # # 172.210.218.144/28

# # # 13.69.67.192/28
# # # 13.69.107.112/28
# # # 13.69.112.128/28
# # # 40.74.24.192/26
# # # 40.74.26.0/23
# # # 40.113.176.232/29
# # # 52.236.187.112/28

# # # Failed to activate network policy: Network policy ALLOW_AEP_IP_ADDRESSES cannot be activated. Requestor IP address/Token, 71.255.62.7, must be included in the allowed_ip_list or allowed network rules. To add the specific IP, execute command "ALTER NETWORK POLICY ALLOW_AEP_IP_ADDRESSES SET ALLOWED_IP_LIST=('71.255.62.7');". Similarly, a CIDR block of IP addresses can be added instead of the specific IP address.

# # # {
# # #         "name": "Chaunceys postgres db",
# # #         "description": "Test connection for PostgreSQL",
# # #         "auth": {
# # #             "specName": "Connection String Based Authentication",
# # #             "params": {
# # #                 "connectionString": "Server=ec2-174-129-100-198.compute-1.amazonaws.com;Database=d20l3o13od4p1i;Port=5432;UID=ewzvvfyghnpnri;Password=64732fe81f123be28aa5b700f74fb9fd48c15d99cfd1ebaa6f2a083d072457dd;EncryptionMethod=1;ValidateServerCertificate=1"
# # #             }
# # #         },
# # #         "connectionSpec": {
# # #             "id": "74a1c565-4e59-48d7-9d67-7c03b8a13137",
# # #             "version": "1.0"
# # #         }
# # #     }