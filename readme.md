LangChain to LangFlow Conversion Code

Description

The LangChain to LangFlow Converter is a program that allows you to seamlessly convert code written in the LangChain framework into code compatible with LangFlow, which is the UI version of the LangChain framework. LangChain is a powerful framework used for developing applications powered by language models, and LangFlow provides a user-friendly interface to interact with those applications.

With this converter, you can easily transform your existing LangChain code into a LangFlow-compatible format and upload it into the LangFlow platform.

How to Use
1.Clone this repository to your local machine:
git clone 

2.Install the required dependencies:
cd langchain_2_langflow
pip install -r requirements.txt

3.Define each model or attribute separately on different lines in input.py.
For example:
recommanded way to provide input 
    llm = OpenAI(temperature=0.8, openai_api_key=key)
    jsonspec = JsonSpec(dict_=dict)
    jsontoolkit = JsonToolkit(spec=jsonspec)
    jsonagent = create_json_agent(toolkit=jsontoolkit, llm=llm)

avoid methods like:
    jsonspec = JsonSpec(dict_=dict)
    jsonagent = create_json_agent(toolkit=JsonToolkit(spec=jsonspec), llm=OpenAI(temperature=0.8, openai_api_key=key))

4.If your LangChain code requires external inputs, specify the path of those inputs relative to a 'inputs' folder
for example
if your input file require a json file(base_flow.json) as a input
    llm = OpenAI(temperature=0.8, openai_api_key=key)
    with open('./inputs/base_flow.json', 'r') as a:
        dict = json.load(a)
    jsonspec = JsonSpec(dict_=dict)
    jsontoolkit = JsonToolkit(spec=jsonspec)
    jsonagent = create_json_agent(toolkit=jsontoolkit, llm=llm)


5.Run the converter script:
streamlit run app.py

The converter will process input.py and generate a JSON file, converted.json,
which will contain the LangFlow-compatible code
Now, you can upload converted.json into the LangFlow platform 
to leverage the UI version of your LangChain application.