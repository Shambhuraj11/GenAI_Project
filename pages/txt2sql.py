from dotenv import load_dotenv
import streamlit as st
import os 
import sqlite3
# import typing
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
groq_api_key= os.environ['GROQ_API_KEY']


qa_template = """
You are an expert data analyst. You have deep knowledge of SQL databse.You are expert in convert English qustion to SQL query. 
Data base information:
    Database name:  STUDENT 
    Columns:  NAME, CLASS , SECTION, MARKS

For Example 
Example 1 - How many entries of records are present?, 
SQL command - SELECT COUNT(*) from STUDENT; 

Example 2 - Tell me all the students studying  in Data  science class?,
SQL Command - SELECT * FROM STUDENT WHERE CLASS="Data Science";

Note - SQL code should not have ''' in beginning or end and sql word in output. 

"""
llm= ChatGroq(model="llama-3.2-3b-preview")
qa_prompt = ChatPromptTemplate.from_messages(
   [ SystemMessagePromptTemplate.from_template(qa_template),
    HumanMessagePromptTemplate.from_template("{input}")
   ]
)


qa_chain = qa_prompt| llm

def llm_reponse(question):
    response = qa_chain.invoke(question)

    return response.content

def read_sql_query(sql_cmd,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql_cmd)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    
    return rows

## Streamlit app

st.set_page_config(page_title="NL2SQL bot")
st.sidebar.header("NL2SQL Bot")
st.header("Text to SQL Bot")

question = st.text_input("INPUT: ",key="input")

submit = st.button("Ask Question")

if submit:
    response = llm_reponse({"input":question})
    print(response)

    data = read_sql_query(response.replace("'''","").replace("```",""),"student.db")

    st.subheader("The Response is")
    if isinstance(data,list):
        for row in data:
            print(row)
            st.subheader(row)
    
    else:
        st.subheader(data)