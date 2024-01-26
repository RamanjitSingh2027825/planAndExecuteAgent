# import packages
from dotenv import load_dotenv
from langchain_openai.chat_models.azure import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tools.sql import describe_database_tool, describe_table_tool, run_query_tool
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import create_openai_functions_agent, AgentExecutor

# load environment variables
load_dotenv()

# create llm model object
llm = AzureChatOpenAI(
    openai_api_version = "2023-09-01-preview",
    azure_deployment= "gpt-35-turbo-16k",
    model_name="gpt-35-turbo-16k"
)

# tool
tools = [describe_table_tool, run_query_tool]

# prompt
system_message = SystemMessage(
    content=f'''You are an AI with access to Tables : Marks, Professors, Subjects, ProfessorSubjects, WeeklySchedule
1. Utilize 'describe_table_tool' to retrieve detailed information about the 'Marks' table. Understand its column names, data types, and potential relationships.
2. Explore the 'Professors' table using 'describe_table_tool.' Gather information about its structure, including column names, data types, and any foreign key relationships.
3. Investigate the 'Subjects' table using 'describe_table_tool' to understand its columns, data types, and potential connections with other tables.
4. Examine the 'ProfessorSubjects' table with 'describe_table_tool,' focusing on its columns, data types, and foreign key relationships.
5. Lastly, explore the 'WeeklySchedule' table using 'describe_table_tool.' Understand its structure, including column names, data types, and potential relationships.

Based on the insights obtained from exploring these tables, formulate a syntactically correct SQLite query.
6. Use 'run_query_tool' to execute the formulated query.

The query should involve at least one of the tables mentioned ('Marks,' 'Professors,' 'Subjects,' 'ProfessorSubjects,' 'WeeklySchedule'). Avoid including any irrelevant columns or tables in your final query.

Test the query's correctness and completeness using theoretical scenarios or sample data.

Your final output should include both the SQLite query and the results obtained from executing the query using 'run_query_tool.' Provide a clear and concise explanation of how the information gathered from 'describe_table_tool' influenced the construction of your query.
'''
)

human_message_prompt = HumanMessagePromptTemplate.from_template(
    template="{input}"
)

prompt = ChatPromptTemplate(
    messages=[
        system_message,
        human_message_prompt,
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

# create agent
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# create agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("################### L A N G C H A I N's P R O J E C T #######################")
query = input("Enter Query : ")
while query!="exit()":
    print(agent_executor.invoke({"input":query}))
    query = input("Enter Query : ")