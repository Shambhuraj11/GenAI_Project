from dotenv import load_dotenv
import streamlit as st
import os 
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader
from langchain_core.output_parsers import StrOutputParser
from app.prompts.ats_prompt import resume_improviser_prompt,resume_matcher_prompt,resume_review_prompt
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
groq_api_key= os.environ['GROQ_API_KEY']

## Streamlit app

st.set_page_config(page_title="ATS Resume Expert", layout="centered")
st.sidebar.header("Resume Expert")
st.header("Application Tracking system with Llama3-70b")

llm = ChatGroq(model="llama3-70b-8192")


def get_pdf_text(pdf):
    """Read PDF and Extract text from Pages"""
    raw_txt = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        txt = page.extract_text()
        if txt:
            raw_txt += txt
    
    # st.write(raw_txt)
    return raw_txt

job_description = st.text_area("Job Description: ",key="input")

resume = st.file_uploader("Upload your Resume (PDF)",type=["pdf"])

if resume is not None:
    st.write("PDF uploaded Successfully.")

    resume_txt = get_pdf_text(resume)

submit_1 = st.button("Review My Resume")

submit_2 = st.button("Percentage Match")

submit_3 = st.button("How can I improvise my skills")

if submit_1:
    if resume is not None:
        chain = resume_review_prompt | llm | StrOutputParser()
        response = chain.invoke({"input":resume_txt})
        st.write(response)
    else:
        st.write("Please upload Resume!!")


if submit_2:
    if resume is not None:
        chain = resume_matcher_prompt| llm | StrOutputParser()
        response = chain.invoke({"input":resume_txt,"content":job_description})
        st.write(response)
    else:
        st.write("Please upload Resume!!")


if submit_3:
    if resume is not None:
        chain = resume_improviser_prompt| llm | StrOutputParser()
        response = chain.invoke({"input":resume_txt,"content":job_description})
        st.write(response)
    else:
        st.write("Please upload Resume!!")

    







