from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from agents.Code_Executor_agent import getCodeExecutorAgent
from agents.Data_Analyzer_agent import getDataAnalyzerAgent
from config.config import TEAM_MAX_TURNS

def getDataAnalyzerTeam(docker,model_client):

    code_executor_agent = getCodeExecutorAgent(docker)

    data_analyzer_agent = getDataAnalyzerAgent(model_client)


    text_mention_termination = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[data_analyzer_agent,code_executor_agent],
        max_turns=TEAM_MAX_TURNS,
        termination_condition=text_mention_termination
    )

    return team