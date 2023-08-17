# Importing packages
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
import pickle


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
    # Creating a title for the web page
    st.header("Chat with your PDF File")



# Running the application
if __name__ == '__main__':
    main()

