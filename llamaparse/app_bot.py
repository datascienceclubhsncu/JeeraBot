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

st.set_page_config(page_title="JEERA-BOT", layout="centered")

# Radio button to select view mode
view_mode = st.radio("Select View Mode:", ("Desktop", "Mobile"))

# Set layout adjustments based on the selected view mode
if view_mode == "Desktop":
    # Desktop layout with centered alignment
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjusted column ratios for Desktop

    with col1:
        st.image("llamaparse/data/Logo_HSNC.png", width=80)

    with col2:
        st.markdown("<h1 style='text-align: center;'>JEERA-BOT</h1>", unsafe_allow_html=True)

    with col3:
        st.image("llamaparse/data/Logo_SAS.png", width=80)

    # Centered description text
    st.markdown("""
    <p style="text-align: center;">
    Hi, this chatbot is made by Members of the Research Cell, School of Applied Sciences, HSNC University, Mumbai. This is a beta version currently in testing, so answers might not be completely accurate. Please share your feedback at <a href="mailto:datascience.club@hsncu.edu.in">datascience.club@hsncu.edu.in</a> or on our LinkedIn page <a href="https://www.linkedin.com/in/r-cell--sas">www.linkedin.com/in/r-cell--sas</a>. Thank you!
    </p>
    """, unsafe_allow_html=True)

elif view_mode == "Mobile":
    # Mobile layout with vertical alignment
    st.image("llamaparse/data/Logo_HSNC.png", width=60)
    st.markdown("<h1 style='text-align: center;'>JEERA-BOT</h1>", unsafe_allow_html=True)
    st.image("llamaparse/data/Logo_SAS.png", width=60)

    # Centered description text for mobile view with smaller font size
    st.markdown("""
    <p style="text-align: center; font-size: 14px;">
    Hi, this chatbot is made by Members of the Research Cell, School of Applied Sciences, HSNC University, Mumbai. This is a beta version currently in testing, so answers might not be completely accurate. Please share your feedback at <a href="mailto:datascience.club@hsncu.edu.in">datascience.club@hsncu.edu.in</a> or on our LinkedIn page <a href="https://www.linkedin.com/in/r-cell--sas">www.linkedin.com/in/r-cell--sas</a>. Thank you!
    </p>
    """, unsafe_allow_html=True)

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
