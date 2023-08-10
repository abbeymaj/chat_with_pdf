from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT =  '-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of packages as defined in the requirements.txt file.
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name='chat_with_pdf',
    version='0.0.1',
    author='Abhijit',
    author_email='abbey.majumdar@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)