from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever


class LLM:
    def __init__(self, vector_db, question):
        self.local_model = "llama3"
        self.llm = ChatOllama(model=self.local_model)
        self.QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five 
            different versions of the given user question to retrieve relevant documents from a
            vector database. By generating multiple perspectives on the user question, your goal
            is to help the user overcome some of the limitations of the distance-based similarity
            search. Provide these alternative questions seperated by newlines.
            Original question: {question},
            """
        )
        self.vector_db = vector_db
        self.question = question

    def get_answer(self):
        retriever = MultiQueryRetriever.from_llm(
            self.vector_db.as_retriever(),
            self.llm,
            prompt=self.QUERY_PROMPT
        )

        # RAG prompt
        template = """Answer the question based ONLY on the following context:
        {context}
        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template=template)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
        )
        response = chain.invoke(self.question)
        return response
