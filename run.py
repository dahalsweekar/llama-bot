from datetime import datetime
from llm.pdf_parser import Parse
from llm.embedding import Embedding
from llm.llm import LLM


class Main:
    def __init__(self, pdf_path):
        self.pdf = pdf_path

    def prepare_data(self):
        # get pdf text chunks
        text_chunks = Parse(pdf_doc=self.pdf).get_text_chunks()
        # create vector sore
        vector_store = Embedding(chunks=text_chunks).get_vectorstore()
        return vector_store


class GR:
    def __init__(self, vector_store, question):
        self.question = question
        self.vector_store = vector_store

    def generate_response(self):
        response = LLM(vector_db=self.vector_store, question=self.question).get_answer()
        return response
