import os
from dotenv import load_dotenv
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import (
    ServiceContext,
    download_loader,
    VectorStoreIndex,
    StorageContext,
    Settings,
    load_index_from_storage,
)
from llama_index.readers.file import HTMLTagReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()


pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
pc_index = pc.Index(host=os.environ.get("PINECONE_HOST"))

Settings.embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="corpu-text-embedding-ada-002",
    api_key=os.getenv("AZURE_API_KEY"),
    azure_endpoint=os.getenv("AZURE_API_BASE"),
    api_version="2023-05-15",
)

Settings.llm = AzureOpenAI(
    model="text-davinci-003",
    deployment_name="corpu-text-davinci-003",
    temperature=0.4,
    api_key=os.getenv("AZURE_API_KEY"),
    azure_endpoint=os.getenv("AZURE_API_BASE"),
    api_version="2023-05-15",
)

if __name__ == "__main__":
    print("Ingesting data...")
    dir_reader = SimpleDirectoryReader(
        input_dir="symspellpy-docs", file_extractor={".html": HTMLTagReader()}
    )
    documents = dir_reader.load_data()
    print(f"Loaded {len(documents)} documents")

    node_parser = SimpleNodeParser.from_defaults(chunk_size=300, chunk_overlap=50)

    vector_store = PineconeVectorStore(pinecone_index=pc_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        show_progress=True,
        storage_context=storage_context,
    )
