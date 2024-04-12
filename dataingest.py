from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS



DB_FAISS_PATH = "./vectorstore/db_faiss"
DATA_DIR = "./data"


# Create vector database
def create_vector_database():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    
    loaded_documents = loader.load()
    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(loaded_documents)

    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )

    # Create and persist a Chroma vector database from the chunked documents
    vector_database = FAISS.from_documents(
        documents=chunked_documents,
        embedding=huggingface_embeddings,
    )

    vector_database.save_local(DB_FAISS_PATH)


if __name__ == "__main__":
    create_vector_database()