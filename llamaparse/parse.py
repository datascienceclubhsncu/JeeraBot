from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#set the embedding settings
Settings.embed_model= HuggingFaceEmbedding(
    model_name="Alibaba-NLP/gte-multilingual-base",
    trust_remote_code=True
)

#set up a parser
parser= LlamaParse(
    result_type='markdown'
)

llm= Groq(
    model="llama3-70b-8192"
)

file_extractor={'.pdf': parser}

sub_doc=SimpleDirectoryReader(input_dir='llamaparse/data', file_extractor=file_extractor)
documents= sub_doc.load_data()

index= VectorStoreIndex.from_documents(documents=documents)

# create a query engine for the index
query_engine = index.as_query_engine(
    llm=llm,
)

if __name__ == '__main__':
    while (prompt := input("Ask anything? ")) !='q':
        response= query_engine.query(prompt)
        print(response.response)
