import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from src.prompt import *
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA


# OpenAI authentication
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ""

    for page in data:
        question_gen += page.page_content
    
    splitter_ques_gen = TokenTextSplitter(
        model_name= "gpt-3.5-turbo",
        chunk_size= 10000,
        chunk_overlap = 200
    )

    chunk_ques_gen = splitter_ques_gen.split_text(question_gen)
   
    document_ques_gen = [Document(page_content=t)for t in chunk_ques_gen]
    splitter_ans_gen = TokenTextSplitter(
        model_name="gpt-3.5-turbo",
        chunk_size=1000,
        chunk_overlap=100
    )
    document_ans_gen = splitter_ans_gen.split_documents(document_ques_gen)
    
    return document_ques_gen, document_ans_gen


def llm_pipeline(file_path):
    document_ques_gen, document_ans_gen = file_processing(file_path)

    llm_ques_gen_pipeline = ChatOpenAI(
        temperature = 0.3,
        model = "gpt-3.5-turbo"
    )
    PROMPT_QUESTION = PromptTemplate(template=prompt_template,input_variables=["text"])
    REFINE_PROMPT_QUESTION = PromptTemplate(template=refine_template,input_variables=["existing_answer", "text"])
    ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline, chain_type="refine",question_prompt=PROMPT_QUESTION, refine_prompt=REFINE_PROMPT_QUESTION, verbose=True)

    ques = ques_gen_chain.run(document_ques_gen)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(document_ans_gen, embeddings)

    llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
    ques_list = ques.split("\n")
    filtered_ques_list = [elem for elem in ques_list if elem.endswith('?') or elem.endswith(".")]
    answer_gen_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen,chain_type="stuff",retriever = vector_store.as_retriever())

    return answer_gen_chain, filtered_ques_list

# path = "../data/SDG.pdf"
# llm_pipeline(path)