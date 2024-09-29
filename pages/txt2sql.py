from dotenv import load_dotenv
import streamlit as st
import os 
from app.src.nl_sql_langchain import invoke_chain
from app.src.sql import db_creator
import pandas as pd
load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_ENDPOINT'] = os.getenv('LANGCHAIN_ENDPOINT')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['PINECONE_API_KEY'] = os.getenv('PINECONE_API_KEY')
groq_api_key= os.environ['GROQ_API_KEY']

## Streamlit app

st.set_page_config(page_title="NL2SQL bot")
st.sidebar.header("NL2SQL Bot")
st.header("Text to SQL Bot")
st.info('Kindly use keywords from uploaded CSV in your Query for better results.', icon="ℹ️")


uploaded_file = st.file_uploader("Upload an Csv file", type=("csv"))
st.write("OR")
sample_file = 'studentdataset.csv'
df = pd.read_csv(f"./data/{sample_file}")

# Display the DataFrame
st.write(df.head(4))

if uploaded_file is not None:
    db_creator(uploaded_file,flag = True)
    st.write("You can ask questions now!!")
else:
    if st.button("Load Sample Data"):
        db_creator(sample_file)
        st.write("You can ask questions now!!")


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app re-run
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Accept user input

if prompt := st.chat_input("What's Up?"):
    # add user msg to chat history
    st.session_state.messages.append({'role':"user","content":prompt})

    # Display user msg in chat msg container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display response in container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            if uploaded_file is not None:
                response = invoke_chain(prompt,st.session_state.messages,uploaded_file.name[:-4])
            else:
                response = invoke_chain(prompt,st.session_state.messages,sample_file[:-4])
            st.markdown(response)
        st.session_state.messages.append({"role":"assitant","content":response})