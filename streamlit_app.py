from turtle import up
import streamlit as st
import asyncio
import os

from teams.analyzer_gpt_team import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_config import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage

st.title("Agentic Data Analyzer GPT by AutoGen")

upload_file = st.file_uploader("Upload a CSV file", type=["csv"])

task = st.chat_input("Enter your tassk here...")


async def run_analyzer_gpt(docker, model_client, task):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, model_client)

        async for message in team.run_stream(task=task):
            st.markdown(f"**{message}")
        
        return None

    except Exception as e:
        st.error(f"Error occured: {e}")

        return e
    
    finally:
        await stop_docker_container(docker)

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

else: 
    st.warning("Please provide your task.")



