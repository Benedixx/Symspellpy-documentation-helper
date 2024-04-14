import os
from dotenv import load_dotenv
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms import openai
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import ServiceContext, download_loader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
pc.Index(host=os.environ.get("PINECONE_HOST"))

if __name__ == "__main__":
    print("Hello, World!")
    print(pc.describe_index("llamaindex-documentation-helper"))