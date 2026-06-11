
import streamlit as st
from langchain_groq import ChatGroq
#from langchain.agents import initialize_agent, AgentType
#from langchain.agents.agent_types import AgentType
#from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
import os
import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage
from langchain import hub
#from langchain.agents import load_tools
#from langchain.agents import Tool
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict
#from langchain.agents import load_tools
#from langchain_community.agent_toolkits.load_tools import load_tools
import getpass
from langchain.utilities import SerpAPIWrapper
#from langchain.agents import initialize_agent
from langchain.chains import ConversationChain
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model = "meta-llama/llama-4-scout-17b-16e-instruct",
    temperature = 0,
    max_tokens = 1024,
    max_retries = 2,
    groq_api_key = GROQ_API_KEY)
conversation = ConversationChain(
    llm = llm,
    verbose = False,
    memory = ConversationBufferMemory())
    

class Chatbot:                     # a class is a user defined datatype, where a name is given to that datatype
    def __init__(self):            # everything inside __init__ will automatically be run when an object is declared
        self.chat_history = []     # 'self' python's internal reference identifier for classes
        self.welcome_message = (
            "Hello! What's on agenda today🗓?")
    def query_response(self,user_query):
        agent_prompt = f"""
        The user is querying the large language model to get relevant answer.
        
        User Query: '{user_query}'

        Follow these below instructions while generating response:
        1. Analyze the user's query carefully.
        2. You can use previous conversational memory to understand the user's query.
        3. Generate appropriate response to the user query. 
        4. Pass the final response as output.
        """
        try:            
            response = conversation.run(agent_prompt)            
            return response
        except Exception as e:
            print(f"Agent Error: {e}")
            return("Sorry! Something went wrong while generating response.")       
    def chat(self, user_query):
        self.chat_history.append(user_query)
        if len(self.chat_history) ==1:
            return(
                f"{self.welcome_message}\n\n"
            )
        response = self.query_response(user_query)
        return response
    
#memory = ConversationBufferMemory(memory_key="chat_history")
#chat_agent = initialize_agent(
#    llm=llm,
#    tool = tools,
#    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
#    verbose=False,
#    memory=memory,
#    handle_parsing_errors=True)

st.set_page_config(
    page_title = "Utility ChatBot",
    page_icon = "🌏")
groq_api_key = st.sidebar.text_input("Access Token🔐", type = "password")
st.title("Utility Based ChatBot🔎")
st.write("Welcome to the utility based conversational ChatBot👨🏼‍💻")

if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# User input
user_query = st.chat_input("Type your message here ....")
# Chat Processing
if user_query:
    # Show user Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_query
        }
    )
    with st.chat_message("user"):
        st.markdown(user_query)
    # Generate Bot Response
    response = st.session_state.bot.chat(user_query)
    # Store Bot Response
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )
    # Display Bot response
    with st.chat_message("assistant"):
        if not groq_api_key.startswith("gsk"):
            st.warning("Please enter your access token..",icon = "⚠")
        if groq_api_key.startswith("gsk"):
            st.markdown(response)
