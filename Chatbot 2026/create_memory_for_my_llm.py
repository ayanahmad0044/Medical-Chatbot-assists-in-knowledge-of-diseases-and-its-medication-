from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

   #  Step 1: Load RAW PDF's

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


DATA_PATH="data/"
def load_pdf_files(data):
   loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
   documents = loader.load()
   return documents

documents = load_pdf_files(data = DATA_PATH)
#print("Length ofPDF pages :", len(documents))



# Step 2: create chunks

def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = create_chunks(extracted_data=documents)
#print("Length of text chunks :", len(text_chunks))



# Step 3: create vector embeddings

def get_embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model = get_embedding_model()

# Step 4: store embeddings in faiss

DB_FAISS_PATH = "vectorestore/db_faiss"
db = FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)
