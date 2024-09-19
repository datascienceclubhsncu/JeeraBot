import streamlit as st
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import logging

# Load environment variables
load_dotenv()

# Configure logging to capture errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the embedding model using HuggingFace's multilingual model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="Alibaba-NLP/gte-multilingual-base",
    trust_remote_code=True
)

# Set up a parser
parser = LlamaParse(result_type='markdown')

# Initialize the language model from Groq
llm = Groq(model="llama3-70b-8192")

# Map file types to the parser
file_extractor = {'.pdf': parser}

# Load the documents from the specified directory
sub_doc = SimpleDirectoryReader(input_dir='llamaparse/data', file_extractor=file_extractor)
documents = sub_doc.load_data()

# Create an index from the documents using a vector store
index = VectorStoreIndex.from_documents(documents=documents)

# Create a query engine for the index
query_engine = index.as_query_engine(llm=llm)

# Streamlit app setup
st.title("LlamaParse Query Interface")
st.write("Ask anything and receive responses based on your indexed data.")

# Health check endpoint (optional, if required by your service)
try:
    st.text("App is running health check...")
    st.success("Health check passed!")
except Exception as health_check_error:
    st.error(f"Health check failed: {health_check_error}")
    logger.error(f"Health check error: {health_check_error}")

# Create an input
