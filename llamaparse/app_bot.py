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

# Lazy load the model to reduce initial load time and cache it
@st.cache_resource(show_spinner=False)
def load_model():
    logger.info("Loading the model...")
    return Groq(model="llama2-7b")  # Using a smaller model for testing

llm = load_model()

# Map file types to the parser
file_extractor = {'.pdf': parser}

# Load documents lazily and cache
@st.cache_resource(show_spinner=False)
def load_documents():
    logger.info("Loading documents from the directory...")
    sub_doc = SimpleDirectoryReader(input_dir='llamaparse/data', file_extractor=file_extractor)
    return sub_doc.load_data()

documents = load_documents()

# Create an index from the documents using a vector store and cache
@st.cache_resource(show_spinner=False)
def create_index():
    logger.info("Creating a vector store index...")
    return VectorStoreIndex.from_documents(documents=documents)

index = create_index()

# Create a query engine for the index
@st.cache_resource(show_spinner=False)
def create_query_engine():
    logger.info("Creating query engine...")
    return index.as_query_engine(llm=llm)

query_engine = create_query_engine()

# Streamlit app setup
st.title("LlamaParse Query Interface")
st.write("Ask anything and receive responses based on your indexed data.")

# Health check (to verify app is running)
try:
    st.text("App is running health check...")
    st.success("Health check passed!")
except Exception as health_check_error:
    st.error(f"Health check failed: {health_check_error}")
    logger.error(f"Health check error: {health_check_error}")

# Create an input box for user questions
user_input = st.text_input("Ask a question:")

# Process the query when the user enters a question
if user_input:
    with st.spinner('Processing your query...'):
        try:
            # Query the model
            response = query_engine.query(user_input)
            # Display the result in the Streamlit app
            st.write("### Response:")
            st.write(response.response)
        except Exception as e:
            st.error(f"An error occurred while querying: {e}")
            logger.error(f"Query error: {e}")

