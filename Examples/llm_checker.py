from langchain.llms import OpenAI
from langchain.chains import LLMCheckerChain

key = "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"
llm = OpenAI(temperature=0.8, openai_api_key=key)
chain = LLMCheckerChain.from_llm(llm=llm)

