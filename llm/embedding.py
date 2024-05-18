from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


class Embedding:
    def __init__(self, chunks):
        self.chunks = chunks

    def get_vectorstore(self):
        vectorstore = Chroma.from_texts(texts=self.chunks,
                                        embedding=OllamaEmbeddings(model="llama3", show_progress=True))
        return vectorstore
