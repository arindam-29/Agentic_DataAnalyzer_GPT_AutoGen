from autogen_agentchat.agents import AssistantAgent
from prompts.data_analyzer_prompt import DATA_ANALYZER_SYSTEM_MESSAGE


def getDataAnalyzerAgent(model_client):
    data_analyzer_agent = AssistantAgent(
        name='Data_Analyzer_Agent',
        model_client=model_client,
        description = 'An Agent that solves Data Analysis problem and provides python code to solve it.',
        system_message=DATA_ANALYZER_SYSTEM_MESSAGE
    )
    return data_analyzer_agent