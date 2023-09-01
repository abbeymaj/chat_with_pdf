# Importing packages
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from src.read_pdf import read_pdf
from src.create_vector_store import create_vector_store
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
    logging.info("Uploading the PDF File")
    pdf_obj = st.file_uploader("Please upload your PDF File below.", type='pdf')
    
    if pdf_obj is not None:
        chunks = read_pdf(pdf_obj)
        vector_store = create_vector_store(pdf_obj=pdf_obj, chunks=chunks)
    
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

