# Importing packages
import sys
import os
import pickle
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from src.logger import logging
from src.exception import CustomException

# Creating a function to build the vector store
def create_vector_store(pdf_obj, chunks):
    try:
        # Creating a vector store path
        logging.info("Creating the path to place the vector store")
        vector_store_name = pdf_obj.name[:-4]
        vector_store_path = os.path.join(os.getcwd(), 'vector_store', f'{vector_store_name}.pkl')
        os.makedirs(vector_store_path, exist_ok=True)
        
        VECTOR_FILE_PATH = os.path.join(vector_store_path, f'{vector_store_name}.pkl')
        
        # Checking if the vector store already exists and if yes reading the vector store
        logging.info("Reading the vector store or creating a new one if not present")
        if os.path.exists(VECTOR_FILE_PATH):
            with open(VECTOR_FILE_PATH, 'rb') as file_obj:
                vector_store = pickle.load(VECTOR_FILE_PATH)
        
        # Else creating the vector store
        else:
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            with open(VECTOR_FILE_PATH, 'wb') as file_obj:
                pickle.dump(vector_store, file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
    return vector_store
    