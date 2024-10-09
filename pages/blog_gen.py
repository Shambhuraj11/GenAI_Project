from dotenv import load_dotenv
import streamlit as st
import os 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
# load_dotenv()

# os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
# os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
# os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
# os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
# os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
# os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
# groq_api_key= os.environ['GROQ_API_KEY']

## Streamlit app

st.set_page_config(page_title="Generate Blogs", layout="centered")
st.sidebar.header("Blog Generator")
st.header("Blog generation with Groq Gemma-2-9b")


input_text = st.text_input("Enter the Blog topic")

sys_prompt_temp = """
You are an expert blog writer. Sole objective of your life is to write expert level blog on provided topic for target audience.You have been recognized by various institution for your work of blog writing. Your expertise lies in writing a blog which can easily consumed expert Researchers, Students and even non- technical common people.
"""

human_prompt_temp = """
You are going to generate a blog for {audience}.Write a blog on topic {input}. Use your whole life expertise in the generation of this blog. You have to write blog of {word} words. 

Before starting be clear about provided topic. If you don't have sufficient knowledge ask user to provide another topic as your experties and knowledge about the topic is not sufficient.

Blog should have well structured paragraphs. Make sure to use proper wordings as per level of understanding of target audience. For example common people don't like technical terms in blog unlike Researchers, Students expect some techincal definations but not too much expert level content.

Never exaggerate things in blog. Points that your are going to mention in blog will be verified by user so you points should be intuitive and easliy cross verifed by user.Never mention about a point for which you are pretty unsure. 
"""



def get_blog(input_text: str,no_words:str,blog_style:str):
    llm = ChatGroq(model="gemma2-9b-it")
    prompt = ChatPromptTemplate(
        [
            ("system",sys_prompt_temp),
            ("human",human_prompt_temp)
        ]
    )

    chain = prompt | llm | StrOutputParser()

    resp = chain.invoke({"input":input_text,"audience":blog_style,"word":no_words})

    return resp



## Creating two more columns for additional 2 fields

col_1, col_2  = st.columns([5,5])

with col_1:
    no_words = st.text_input("No of Words")

with col_2:
    blog_style = st.selectbox("Writin the blog for",("Researchers","Students","Common People"),index=0)

submit_button = st.button("Submit")

if submit_button:
    with st.spinner("Working on it..."):
        blog = get_blog(input_text,no_words,blog_style)

        st.write(blog)



