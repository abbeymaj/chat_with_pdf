# Importing packages
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from src.logger import logging


# Locating dotenv 
load_dotenv(find_dotenv())

# Creating a left rail for the web page
with st.sidebar:
    # Creating a title for the left rail
    st.title("My LLM App")
    # Creating a small description for the left rail
    st.markdown('''
                This simple application is powered by a LLM chatbot and is built using the following:
                - [Langchain](https://python.langchain.com)
                - [streamlit](https://streamlit.io)
                ''')

# Creating a the "main" function:
def main():
    '''
    This is the main function which creates a webpage that allows a user to upload a PDF file and chat with it.
    
    '''
    # Creating a title for the web page
    st.header("Chat with your PDF File")
    
    # Upload a PDF File
    logging.info("Uploading and reading the PDF File")
    pdf = st.file_uploader("Please upload your PDF File below.", type='pdf')
    
    # Read the PDF file and extract the text from the document
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)
        
        # Defining the vector store name variable
        logging.info("Creating the vector store")
        vec_store_name = pdf.name[:-4]
        
        # Checking if the vector store already exists and if yes reading the vector store
        if os.path.exists(f'{vec_store_name}.pkl'):
            with open(f'{vec_store_name}.pkl', 'rb') as file_obj:
                vector_store = pickle.load(file_obj)
        # Else creating the vector store
        else:
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f'{vec_store_name}.pkl', 'wb') as file_obj:
                pickle.dump(vector_store, file_obj)
        
        # Allow the user to enter questions to query the PDF file
        question = st.text_input("Ask a question to your PDF File:")
        
        if question:
            documents = vector_store.similarity_search(query=question, k=3)
            llm = OpenAI()
            chain = load_qa_chain(llm=llm, chain_type='stuff')
            with get_openai_callback() as cb:
                response = chain.run(input_documents=documents, question=question)
            st.write(response)
        
# Running the application
if __name__ == '__main__':
    main()

