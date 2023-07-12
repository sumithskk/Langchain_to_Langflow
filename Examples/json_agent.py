import json
from langchain.agents import create_json_agent
from langchain.tools.json.tool import JsonSpec
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.llms import OpenAI


key = "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"
llm = OpenAI(temperature=0.8, openai_api_key=key)
with open('./Base_flows/base_flow.json', 'r') as a:
    dict = json.load(a)
jsonspec = JsonSpec(dict_=dict)
jsontoolkit = JsonToolkit(spec=jsonspec)
jsonagent = create_json_agent(toolkit=jsontoolkit, llm=llm)