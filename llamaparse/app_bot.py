import streamlit as st
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load environment variables
load_dotenv()

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
            st.error(f"An error occurred: {e}")

