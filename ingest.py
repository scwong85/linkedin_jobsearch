import os
import warnings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    UnstructuredURLLoader, DirectoryLoader
)
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import sys

warnings.simplefilter("ignore")




# Create vector database
def create_vector_database(llm_model):
    """
    Creates a vector database using document loaders and embeddings.

    This function loads files,
    splits the loaded documents into chunks, transforms them into embeddings using OllamaEmbeddings,
    and finally persists the embeddings into a Chroma vector database.

    """
    
    ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
    DB_DIR: str = os.path.join(ABS_PATH, f"dburl_{llm_model}")

    # Initialize Ollama Embeddings
    ollama_embeddings = OllamaEmbeddings(model=llm_model)
    loader = DirectoryLoader("skills_data", glob="*.txt")
    data = loader.load()
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=40)
    docs = text_splitter.split_documents(data)
    vectordb = Chroma.from_documents(documents=docs, 
                    embedding=ollama_embeddings,
                    persist_directory=DB_DIR)
    vectordb.persist()


if __name__ == "__main__":
    create_vector_database(sys.argv[1])