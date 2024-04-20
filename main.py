import os
from dotenv import load_dotenv
from pinecone import Pinecone
import streamlit as st
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore

load_dotenv()


@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:
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
    vector_store = PineconeVectorStore(pinecone_index=pc_index)

    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


index = get_index()
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

st.set_page_config(
    page_title="Sysmpellpy Docs helper",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Sysmpellpy Docs helper 📚")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm here to help you with Sysmpellpy documentation. How can I help you today?",
    }]
    
if prompt := st.chat_input("your question"):
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt
    })
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])        

if st.session_state["messages"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(message=str(prompt))
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)