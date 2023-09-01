import sys
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.logger import logging
from src.exception import CustomException


# Creating a function to read the pdf file
def read_pdf(pdf):
    '''
    This function reads the PDF file and breaks the file into chunks
    ================================================
    Parameters:
        pdf - PDF Object
    
    ------------------------------------------------
    
    Returns:
        chunks - Chunks of the PDF File
    
    ================================================
    '''
    logging.info("Reading the PDF file")
    try:
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
    except Exception as e:
        raise CustomException(e, sys)
        
    return chunks