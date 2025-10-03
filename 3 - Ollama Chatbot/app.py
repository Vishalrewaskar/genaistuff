import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

import os
from dotenv import load_dotenv
load_dotenv()

## Langchain Tracking
# Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot using Ollama"


# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistance. Please response to the user queries."),
        ("user", "question:{question}")
    ]
)

def genarate_respnse(question, engine, temperature, max_tokens):
    llm = Ollama(model=engine)
    output_parser = StrOutputParser()
    chain = prompt | llm |output_parser
    answer = chain.invoke({'question':question})
    return answer



## select various Open source  model which are availble locally
engine = st.sidebar.selectbox("Select your Open source model", ['gemma3:1b', 'llama3.2'])

# Adjust responce parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_token = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You: ")

if user_input :
    response = genarate_respnse(user_input,engine, temperature, max_token)
    st.write(response)
else: 
    st.write("Please provide the query")

