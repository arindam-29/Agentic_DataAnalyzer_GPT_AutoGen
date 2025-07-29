import streamlit as st
import asyncio
import os

from teams.analyzer_gpt_team import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_config import getDockerCommandLineExecutor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("Agentic Data Analyzer GPT by AutoGen")

upload_file = st.file_uploader("Upload a CSV file", type=["csv"])

task = st.chat_input("Enter your tassk here...")

# Streamlit variables to save messages and state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if 'images_shown' not in st.session_state:
    st.session_state.images_shown=[]

async def run_analyzer_gpt(docker, model_client, task):
    
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, model_client)

        if st.session_state.autogen_team_state is not None:             #Load earlier state
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                if message.source.startswith("user"):
                    with st.chat_message("User"):
                        st.markdown(message.content)
                elif message.source.startswith("Data_Analyzer_Agent"):
                    with st.chat_message("Data Analyzer"):
                        st.markdown(message.content)
                elif message.source.startswith("Python_Code_Executor_Agent"):
                    with st.chat_message("Code Executor"):
                        st.markdown(message.content)
                st.session_state.messages.append(message.content)       #Save all messages

            elif isinstance(message, TaskResult):
                st.markdown(f"Stop Reason: {message.stop_reason}")
                st.session_state.messages.append(message.stop_reason)

        st.session_state.autogen_team_state = await team.save_state()   #Save state

        return None

    except Exception as e:
        
        st.error(f"Error occured: {e}")

        return e
    
    finally:
        await stop_docker_container(docker)

# Check if messages present?
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
    if upload_file is not None and task:

        if not os.path.exists("working_dir"):
            os.makedirs("working_dir")

        with open("working_dir/data.csv", 'wb') as f:
            f.write(upload_file.getbuffer())
        
        model_client=get_model_client()
        docker=getDockerCommandLineExecutor()

        error =asyncio.run(run_analyzer_gpt(docker, model_client, task))

        if error:
            st.error(f"An Error occured! {error}")
        
    else:
        st.warning("Please upload the file before requesting for any task!")

    if os.path.exists("working_dir/output.png"):
        st.image("working_dir/output.png", caption="Output Image")

else: 
    st.warning("Please provide your task.")