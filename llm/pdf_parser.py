from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


class Parse:
    def __init__(self, pdf_doc):
        self.pdf_doc = pdf_doc
        self.text = ""

    def get_pdf_text(self):
        pdf = PdfReader(self.pdf_doc)
        for page in pdf.pages:
            self.text += page.extract_text()

    def get_text_chunks(self):
        self.get_pdf_text()
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(self.text)
        return chunks
