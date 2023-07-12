from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


key = "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"
llm = OpenAI(temperature=0.8, openai_api_key=key)
prompt = PromptTemplate(
    input_variables=["product"],
    template="I want you to act as a naming consultant for new companies\
                        What is a good name for a company that makes {product}?"
)
chain = LLMChain(llm= llm, prompt=prompt)