from autogen_agentchat.agents import CodeExecutorAgent

def getCodeExecutorAgent(code_executor):

    code_executor_agent = CodeExecutorAgent(
        name='Python_Code_Executor_Agent',
        code_executor=code_executor
    )

    return code_executor_agent