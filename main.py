from pprint import pprint
import json
import copy
import inspect
import langchain
import importlib.util
import streamlit as st
import pandas as pd
from langchain_to_langflow import (
    get_template,
    get_base_class,
    allocate_components,
    get_children,
    get_edge,
    get_vertex_agent_arg,
    get_vertex_arguments,
    is_instance_from_langchain,
    print_vertex_and_edges
)

all_vertex_info = {}

# input file path
PYTHON_FILE_PATH = "qwerty1234567890.py"


# get classes and instances from the input file
module_name = "custom_module"
spec = importlib.util.spec_from_file_location(module_name, PYTHON_FILE_PATH)
custom_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custom_module)


# get class objects
class_list = []
function_list = []
other_type_list = []
for name, obj in custom_module.__dict__.items():
    if inspect.isclass(obj):
        class_list.append(obj)
    elif inspect.isfunction(obj):
        function_list.append(obj)
    else:
        pass


# get instances
all_instances = []
for name, obj in custom_module.__dict__.items():
    if is_instance_from_langchain(type(obj), "langchain") and not isinstance(obj, type):
        all_instances.append(obj)




# base json
base_class = get_base_class()
postion = allocate_components(len(all_instances))
function_list1 = copy.copy(function_list)
for i, y in zip(all_instances, postion):
    lc_kwargs = None
    try:
        if i._lc_kwargs:
            lc_kwargs = i._lc_kwargs
        elif i.lc_kwargs:
            lc_kwargs = i.lc_kwargs
        else:
            pass
    except:
        pass
    # Agents

    if i.__class__.__name__ == "ZeroShotAgent":
        base_class["data"]["nodes"].append(
            get_template("agents", "ZeroShotAgent", y, lc_kwargs, i,all_vertex_info)
        )
    if i.__class__.__name__ == "AgentExecutor":
        all_agents = dir(langchain.agents)
        for j in function_list:
            if j.__name__ in all_agents:
                func_name = j.__name__.split("_")
                func_name = "".join(func_name[1:])
                base_class["data"]["nodes"].append(
                    get_template("agents", func_name, y, lc_kwargs, i,all_vertex_info)
                )
                function_list.remove(j)
                break

    # Chains
    if i.__module__.startswith("langchain.chains"):
        base_class["data"]["nodes"].append(
            get_template("chains", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )

    # Loaders

    elif i.__module__.startswith("langchain.document_loaders"):
        base_class["data"]["nodes"].append(
            get_template("documentloaders", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )

    # Embeddings
    elif i.__module__.startswith("langchain.embeddings"):
        base_class["data"]["nodes"].append(
            get_template("embeddings", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # LLms
    elif i.__module__.startswith("langchain.llms") or i.__module__.startswith("langchain.chat_models") :
        base_class["data"]["nodes"].append(
            get_template("llms", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Memories
    elif i.__module__.startswith("langchain.memory"):
        base_class["data"]["nodes"].append(
            get_template("memories", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Prompts
    elif i.__module__.startswith("langchain.prompts"):
        base_class["data"]["nodes"].append(
            get_template("prompts", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # TextSplitters
    elif i.__module__.startswith("langchain.text_splitter"):
        base_class["data"]["nodes"].append(
            get_template("textsplitters", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # ToolKits
    elif i.__module__.startswith("langchain.agents.agent_toolkits"):
        base_class["data"]["nodes"].append(
            get_template("toolkits", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Tools
    elif i.__module__.startswith("langchain.tools"):
        base_class["data"]["nodes"].append(
            get_template("tools", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Utilities
    elif i.__module__.startswith("langchain.utilities"):
        base_class["data"]["nodes"].append(
            get_template("utilities", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Vectors Stores
    elif i.__module__.startswith("langchain.vectorstores"):
        base_class["data"]["nodes"].append(
            get_template("vectorstores", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )
    # Wrappers
    elif i.__module__.startswith("langchain.requests"):
        base_class["data"]["nodes"].append(
            get_template("wrappers", i.__class__.__name__, y, lc_kwargs, i,all_vertex_info)
        )

    else:
        pass
get_children(all_instances, function_list1,all_vertex_info)


for vertex in all_instances:
    if vertex.__class__.__name__ == "AgentExecutor":
        get_vertex_agent_arg(vertex, all_instances, function_list1,all_vertex_info)
    else:
        get_vertex_arguments(vertex, all_instances,all_vertex_info)
edges = get_edge(all_vertex_info)


base_class["data"]["edges"] = edges
# pprint(all_vertex_info, sort_dicts=False)
print_vertex_and_edges(edges, all_instances, function_list1)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


with open("converted.json", "w") as flow:
    json.dump(base_class, flow, cls=SetEncoder)
# pprint(base_class, sort_dicts=False)
