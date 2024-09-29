from langchain_core.prompts import ChatPromptTemplate,PromptTemplate \
,FewShotChatMessagePromptTemplate,MessagesPlaceholder


## Adding few shot examples
examples = [
    {
        "input":"How many entries of records are present?",
        "query":"SELECT COUNT(*) from STUDENT;"
    },
    {
        "input":"Tell me all the students studying  in Data  science class?",
        "query":"SELECT * FROM STUDENT WHERE CLASS='Data Science';"
    },
    {
        "input":"Tell me number of the students studying in all class?",
        "query":"SELECT count(*) FROM STUDENT;"
    },
    {
        "input":"Tell me name of the students studying in mba class?",
        "query":"SELECT NAME FROM STUDENT where class='MBA';"
    }
]

example_prompt = ChatPromptTemplate.from_messages(
     [
         ("human", "{input}\nSQLQuery:"),
         ("ai", "{query}"),
     ]
 )
few_shot_prompt = FewShotChatMessagePromptTemplate(
     example_prompt=example_prompt,
     examples=examples,
     input_variables=["input","top_k",'table_info']
 )

# Query generation prompt
sql_chain_prompt = ChatPromptTemplate.from_messages(
     [
         ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
         few_shot_prompt,
        MessagesPlaceholder(variable_name='messages'),
         ("human", "OutPut should only Contain SQL query and Nothing else and nothing else associated with it.Never provide ```sql and ``` at start and end of query.\n {input}"),
     ]
 )

# Answer rephrasing prompt
sql_answer_rephrase_prompt = PromptTemplate.from_template("""
Given the following user question, corresponding sql query, and SQL result. Answer from user point of view and avoid mention of SQL query
If you don't find the answer ask user to repharse question.
Question:{question}
SQL_query:{query}
SQL_Result:{result}
Answer:
""")
