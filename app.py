# Importing packages
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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
        
        # Creating embeddings
        
        
# Running the application
if __name__ == '__main__':
    main()

