from app.prompts.sql_prompt import sql_chain_prompt,sql_answer_rephrase_prompt
import streamlit as st 
from langchain_community.utilities.sql_database import SQLDatabase
from pyprojroot import here # IMP
from langchain_groq import ChatGroq
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain.memory import ChatMessageHistory


@st.cache_resource
def get_chain(file_name):
    print("Creating Txt2SQL Chain")
    db_path = str(here("data")) + f"/{file_name}.db"
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    llm = ChatGroq(model="gemma2-9b-it")
    generate_query = create_sql_query_chain(llm,db,sql_chain_prompt)
    
    execute_query = QuerySQLDataBaseTool(db=db)

    rephrase_answer = sql_answer_rephrase_prompt | llm | StrOutputParser()

    final_chain = (
        RunnablePassthrough.assign(query = generate_query).assign(result = itemgetter("query")|execute_query)
    )| rephrase_answer

    return final_chain

def create_history(messages):
    history = ChatMessageHistory()
    for msg in messages:
        if msg['role'] == "user":
            history.add_user_message(msg['content'])
        else:
            history.add_ai_message(msg['content'])

    return history       

def invoke_chain(question,messages,file_name):
    chain = get_chain(file_name)
    history = create_history(messages)
    try:
        response = chain.invoke({"question":question,"messages":history.messages})
    except Exception as err:
        response = "I'm not able to process your query can you repharase your query!!"
    history.add_user_message(question)
    history.add_ai_message(response)
    return response
