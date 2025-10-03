import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

# Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot using OpenAI"

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistance. Please response to the user queries."),
        ("user", "question:{question}")
    ]
)

def genarate_respnse(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain = prompt | llm |output_parser
    answer = chain.invoke({'question':question})
    return answer

## title of the app
st.title("Enhanced Q&A Chatbot using OpenAI")

## Sidebar for setting
st.sidebar.title("Setting")
api_key = st.sidebar.text_input("Enter your openAI API key: ", type='password')

## drop down to select various OpenAI  model
llm = st.sidebar.selectbox("Select your OpenAI model", ['gpt-4o', 'gpt-4-turbo', 'gpt-4'])

# Adjust responce parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_token = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

## main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You: ")

if user_input:
    response = genarate_respnse(user_input, api_key, llm, temperature, max_token)
    st.write(response)
else:
    st.write("Please provide the query")

