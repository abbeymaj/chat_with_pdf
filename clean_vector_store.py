# Importing packages
import os
import sys
import time
from src.exception import CustomException
from src.logger import logging

# Creating a function to remove any .pkl files that are older than 30 days from the vector store
def clean_vector_store():

    # Fetching current time
    now = time.time()

    # Removing and .pkl files that are older than 30 days
    try:
        # Defining the path
        path = 'vector_store'
        
        # List all files in the directory
        for f in os.listdir(path):
            
            # If a file extension is .pkl, join it with the main path
            if str(f).endswith('.pkl'):
                f_path = os.path.join(path, f)
                
                # If the file was last modified 30 days ago, remove the file
                if os.stat(f_path).st_mtime < now - (30 * 86400):
                    logging.info('Removing .pkl files older than 30 days')
                    os.remove(f_path)
                    logging.info('Files older than 30 days removed')
            
    except Exception as e:
        raise CustomException(e, sys)
    

if __name__ == '__main__':
    clean_vector_store()