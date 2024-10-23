CHAUNCEY PLUMMER – TAP CXM

RAG Application for Adobe Campaign Classic Documentation
This repository contains a Retrieval-Augmented Generation (RAG) application designed to assist users in answering questions related to Adobe Campaign Classic documentation. The application works by vectorizing the Adobe Campaign Classic documentation, storing it in MongoDB, and using a vector search to retrieve relevant information based on user input. It then leverages Ollama to read and provide accurate answers from the retrieved documentation.

Table of Contents
Features
Architecture
Setup
Usage
Contributing
License
Features
Vectorized Documentation: The Adobe Campaign Classic documentation is vectorized for efficient search.
MongoDB Storage: All vectorized data is stored in a MongoDB database for scalable retrieval.
Vector Search: User input is used to search the vectorized data, ensuring that relevant documentation is retrieved.
Ollama Integration: After retrieving the relevant documents, the system uses Ollama to read and answer questions in natural language.
Architecture
The system is composed of two main components:

Vectorization and Storage:

Adobe Campaign Classic documentation is vectorized using embeddings.
The vectorized data is stored in MongoDB for efficient retrieval.
User Query and Response:

A Python script takes user input, vector searches the MongoDB database, and retrieves relevant documentation.
Ollama processes the retrieved information and provides a concise, natural-language answer to the user's query.
Workflow
Documentation data is vectorized and stored in MongoDB.
User inputs a question or search query.
The application vectorizes the input and performs a search on the MongoDB database.
The most relevant documents are retrieved.
Ollama processes the documents and generates an answer based on the retrieved content.
Setup
Prerequisites
Python 3.8+
MongoDB
Ollama
Required Python libraries: pymongo, sentence-transformers, ollama, and numpy
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/chaunceyTAP/AI.git
cd AI
Install the necessary dependencies:

bash
Copy code
pip install -r requirements.txt
Set up MongoDB:

Ensure MongoDB is running on your local machine or connect to a remote MongoDB instance.
Update the MongoDB connection string in the configuration file if necessary.
Download or gather Adobe Campaign Classic documentation.

Run the script to vectorize and store the documentation in MongoDB:

bash
Copy code
python vectorize_docs.py
Usage
Run the main application to answer user queries:

bash
Copy code
python query_docs.py
Input your question when prompted, and the application will return an answer based on the Adobe Campaign Classic documentation.

Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue.

License
This project is licensed under the MIT License.
