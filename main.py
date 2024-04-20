import os
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore


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
    temperature=0,
    api_key=os.getenv("AZURE_API_KEY"),
    azure_endpoint=os.getenv("AZURE_API_BASE"),
    api_version="2023-05-15",
)

if __name__ == "__main__":
    query = "how do i load dictionary on symspellpy?"
    vector_store = PineconeVectorStore(pinecone_index=pc_index)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    print(response)
    for i in response.metadata.items():
        file_name = i[1]['file_name']
        print("reference used : ", file_name)