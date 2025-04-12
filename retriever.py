from mistralai import Mistral

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

import numpy as np
import os 

from helper import get_env, file_helper


print( "Triggered retreiver" )

# GET API KEY
MISTRAL_API_KEY = get_env.retreive_value( "MISTRAL_API_KEY")

#CALL AI SERVICE 
client = Mistral( api_key = MISTRAL_API_KEY )


def RETRIEVER ():   
    
    
    KNOWLEDGE_BASE_PATH = get_env.retreive_value("KNOWLEDGE_BASE_PATH") # PRO 
    # KNOWLEDGE_BASE_PATH = get_env.retreive_value("KNOWLEDGE_BASE_PATH_TEST") # TEST 
    
    KNOWLEDGE_BASE_VECTOR_PATH = get_env.retreive_value("KNOWLEDGE_BASE_VECTOR_PATH")
    
    loader = TextLoader(file_path= KNOWLEDGE_BASE_PATH, encoding="utf-8")
    KNOWLEDGE_BASE = loader.load()
        
    ##### SPLIT TEXT INTO CHUNK #####
    #TEXT CHOPPER
    # Splits the loaded knowledge base into smaller chunks of 800 characters with a 100-character overlap. This ensures that no information is lost between chunks.
    text_chopper = RecursiveCharacterTextSplitter(
                    chunk_size=800,
                    chunk_overlap=100, 
                    separators=["\n\n", "\n", "\\.", " ", ""]
                )
    # CHOP TEXT INTO CHUNK
    chops = text_chopper.split_documents( KNOWLEDGE_BASE ) 
    
    # SELECT MODEL FOR EMBEDDING
    SELECTED_MODEL_EMBEDDING = "mistral-embed"
     
    # EMBEDDED CHOPPED TEXT CHUNKS
    EMBEDDED = client.embeddings.create(
        model  = SELECTED_MODEL_EMBEDDING,
        inputs = chops[0].page_content
    )    
    
    # STORE INTO VECTOR DB 
    # https://github.com/langchain-ai/langchain/issues/11665
    if not os.path.exists(KNOWLEDGE_BASE_VECTOR_PATH):
        vectordb = Chroma.from_documents(
                            documents = chops,
                            embedding = EMBEDDED,
                            persist_directory = "./vector_db"
        )
      
  
RETRIEVER()


## DESCRIPTION
# The retriever retrieves relevant chunks of text (context) from the vector database based on the input query.
# These chunks are passed to the prompt_template and then to the chat_model for generating a response.