from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.readers.json import JSONReader

def load_document(file_name):
    # Initialize JSONReader
    reader = JSONReader(levels_back=0)

    # Load data from JSON file
    documents = reader.load_data(input_file=f".\\data\\mbpp\\testless\\{file_name}-no-tests.json", extra_info={})
    return documents

def set_up_llama(documents):    
    # bge-base embedding model
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    Settings.llm = Groq(model="llama-3.1-70b-versatile")
    index = VectorStoreIndex.from_documents(
        documents,
    )
    query_engine = index.as_query_engine()
    return query_engine

query_engine = set_up_llama(load_document('train-00000-of-00001'))
print(query_engine.query(f"""Read all the code present in the key 'code' of task id number 601 and try to understand it completely. Then, create five assert test cases for it.
            Your output must be the code, only. Do no print 'output' in your output, ASSERTS ONLY. Use techniques like edge cases, line coverage, branch coverage, path coverage and loop testing. Do not comment on the code or surround it by backsticks.
            """))
