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

# Set the embedding model using a smaller HuggingFace model to save resources
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    trust_remote_code=False  # Not needed for this smaller model
)

# Set up a parser
parser = LlamaParse(result_type='markdown')

# Lazy load the model to reduce initial load time and cache it
@st.cache_resource(show_spinner=False)
def load_model():
    logger.info("Loading the model...")
    # Replace 'valid-model-name' with a correct, available model name
    return Groq(model="llama3-70b-8192")

llm = load_model()

# Map file types to the parser
file_extractor = {'.pdf': parser, '.xlsx': parser}

# Load documents lazily and cache
@st.cache_resource(show_spinner=False)
def load_documents():
    try:
        logger.info("Loading documents from the directory...")
        sub_doc = SimpleDirectoryReader(input_dir='llamaparse/data', file_extractor=file_extractor)
        return sub_doc.load_data()
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        st.error(f"Error loading documents: {e}")
        return []

documents = load_documents()

# Create an index from the documents using a vector store and cache
@st.cache_resource(show_spinner=False)
def create_index():
    if not documents:
        return None
    logger.info("Creating a vector store index...")
    return VectorStoreIndex.from_documents(documents=documents)

index = create_index()

# Create a query engine for the index
@st.cache_resource(show_spinner=False)
def create_query_engine():
    if not index:
        return None
    logger.info("Creating query engine...")
    return index.as_query_engine(llm=llm)

query_engine = create_query_engine()

# Streamlit app setup
st.set_page_config(page_title="JEERA-BOT", layout="wide")  # Wide layout for better alignment

# Top section with logos
col1, col2, col3 = st.columns([1, 6, 1])  # Adjust column ratios

with col1:
    st.image("llamaparse/Logo.png", use_column_width=True)  # Left logo

with col3:
    st.image("llamaparse/Logo_SAS.png", use_column_width=True)  # Right logo

# Title in the center
st.markdown(
    """
    <h1 style='text-align: center; margin-top: -50px;'>JEERA-BOT (Joint Exploration and Evaluation of Resources and Analytics)</h1>
    """,
    unsafe_allow_html=True,
)

# Informational message below the title
st.markdown(
    """
    <div style='text-align: center; font-size: 16px; margin-bottom: 20px;'>
        Hi, this chatbot is made by Members of the Research Cell, School of Applied Sciences, HSNC University, Mumbai. 
        This is a beta version currently in testing, so answers might not be completely accurate. 
        Please share your feedback at <b>datascience.club@hsncu.edu.in</b> or on our LinkedIn page 
        <a href='https://www.linkedin.com/in/r-cell--sas' target='_blank'>www.linkedin.com/in/r-cell--sas</a>. Thank You!
    </div>
    """,
    unsafe_allow_html=True,
)

# Input box for user query
user_input = st.text_input("Ask a question:")

# Process the query when the user enters a question
if user_input and query_engine:
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
else:
    if not query_engine:
        st.warning("Unable to process your query due to document load failure or API rate limit exceeded.")


