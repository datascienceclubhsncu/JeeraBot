import streamlit as st
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import logging
import openpyxl

# Load environment variables
load_dotenv()

# Configure logging to capture errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the embedding model using a smaller HuggingFace model to save resources
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    trust_remote_code=False
)

# Set up a parser
parser = LlamaParse(result_type='markdown')

@st.cache_resource(show_spinner=False)
def load_model():
    logger.info("Loading the model...")
    return Groq(model="llama3-70b-8192")

llm = load_model()

file_extractor = {'.pdf': parser, '.xlsx': parser}

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

@st.cache_resource(show_spinner=False)
def create_index():
    if not documents:
        return None
    logger.info("Creating a vector store index...")
    return VectorStoreIndex.from_documents(documents=documents)

index = create_index()

@st.cache_resource(show_spinner=False)
def create_query_engine():
    if not index:
        return None
    logger.info("Creating query engine...")
    return index.as_query_engine(llm=llm)

query_engine = create_query_engine()

st.set_page_config(page_title="JEERA-BOT", page_icon="🤖", layout="wide")

# Align logos at the top with proper sizing
st.markdown(
    """
    <style>
        .logo-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .logo {
            max-height: 80px;
        }
        .center-text {
            text-align: center;
            margin-top: 20px;
            font-size: 16px;
        }
        .title {
            text-align: center;
            font-weight: bold;
            font-size: 36px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logos
st.markdown(
    """
    <div class="logo-container">
        <img src="llamaparse/Logo.png" class="logo">
        <img src="llamaparse/Logo_SAS.png" class="logo">
    </div>
    """,
    unsafe_allow_html=True,
)

# Title and introduction
st.markdown(
    """
    <div class="title">JEERA-BOT(Joint Exploration and Evaluation of Resources and Analytics)</div>
    <div class="center-text">
        Hi, this chatbot is made by Members of the Research Cell, School of Applied Sciences, HSNC University, Mumbai. 
        This is a beta version currently in testing, so answers might not be completely accurate. Please share your feedback at 
        <b>datascience.club@hsncu.edu.in</b> or on our LinkedIn page: 
        <a href="https://www.linkedin.com/in/r-cell--sas" target="_blank">www.linkedin.com/in/r-cell--sas</a>. Thank You!
    </div>
    """,
    unsafe_allow_html=True,
)

# Input box for questions
user_input = st.text_input("Ask a question:")

if user_input and query_engine:
    with st.spinner('Processing your query...'):
        try:
            response = query_engine.query(user_input)
            st.write("### Response:")
            st.write(response.response)
        except Exception as e:
            st.error(f"An error occurred while querying: {e}")
            logger.error(f"Query error: {e}")
else:
    if not query_engine:
        st.warning("Unable to process your query due to document load failure or API rate limit exceeded.")



