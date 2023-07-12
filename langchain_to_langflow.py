import math
import uuid
import string
import random
import typing
import langchain
from pprint import pprint
from langchain.agents import *
from inspect import signature
from langflow.utils.util import get_base_classes
from langflow.interface.types import build_langchain_types_dict
import pandas as pd
import streamlit as st

all_vertex_template = build_langchain_types_dict()
all_vertex_info = {}


def is_instance_from_langchain(class_obj, module_name):
    try:
        class_module_parts = class_obj.__module__.split(".")
        # Compare the last parts of the module names
        if module_name in class_module_parts:
            return True
        else:
            return False
    except:
        return False


def get_vertex_arguments(vertex, vertices):
    for key, val in vertex.__dict__.items():
        try:
            if val in vertices:
                val_type = typing.get_type_hints(vertex.__class__)[key]
                if typing.get_origin(val_type) is typing.Union:
                    val_type = typing.get_args(val_type)[0]
                all_vertex_info[get_vertex_data(vertex)]["args"].append({key: val_type})
        except:
            pass


def get_vertex_agent_arg(vertex, vertices, function_list):
    all_agents = dir(langchain.agents)
    for function in function_list:
        if function.__name__ in all_agents:
            function_name = function.__name__
            func = globals()[function_name]
            sig = signature(func)
            arguments_type = [
                (arg.name, arg.annotation) for arg in sig.parameters.values()
            ]
            for vert in vertices:
                base_class = get_base_classes(vert.__class__)
                for arg_name, arg_type in arguments_type:
                    if arg_type.__name__ in base_class:
                        val_type = typing.get_type_hints(function)[arg_name]
                        all_vertex_info[get_vertex_data(vertex)]["args"].append(
                            {arg_name: val_type}
                        )


def target_handle_base_type(vertex_name, val):
    return all_vertex_template[val["component_name"]][val["vertex_name"]]["template"][
        vertex_name
    ]["type"]


def get_target_handle(child, key, val):
    target_handle = ""
    base_class = all_vertex_info[child]["base_class"]

    for arg in val["args"]:
        for key1, value in arg.items():
            if value.__name__ in base_class:
                target_handle = f"{target_handle_base_type(key1, val)}|{key1}"
    target_handle = f"{target_handle}|{key}"
    return target_handle


def get_edge(all_vertex_info):
    edges_data = []
    for key, val in all_vertex_info.items():
        if val["children"]:
            for child in val["children"]:
                edge = {
                    "source": child,
                    "sourceHandle": "",
                    "target": "",
                    "targetHandle": "",
                    "style": {"stroke": "inherit"},
                    "className": "stroke-gray-900 dark:stroke-gray-200",
                    "animated": False,
                    "id": "",
                }
                source_baseclass = "|".join(all_vertex_info[child]["base_class"])
                edge[
                    "sourceHandle"
                ] = f"{all_vertex_info[child]['vertex'].__class__.__name__}|{child}|{source_baseclass}"
                edge["target"] = key
                edge["targetHandle"] = f"{get_target_handle(child, key, val)}"

                edges_data.append(edge)

    return edges_data


def get_vertex_data(vertex):
    # print(vertex)
    # print(vertex[1].__class__.__name__)
    for key, val in all_vertex_info.items():
        try:
            if val["vertex"] == vertex:
                return key
        except:
            if val["vertex"] is vertex:
                return key


def get_function_arg_type(function, all_instance) -> list:
    # edge_update = {}
    edge = []
    function_name = function.__name__
    func = globals()[function_name]
    sig = signature(func)
    arguments_type = [(arg.name, arg.annotation) for arg in sig.parameters.values()]
    for i in all_instance:
        base_class = get_base_classes(i.__class__)
        for arg_name, arg_type in arguments_type:
            if arg_type.__name__ in base_class:
                edge.append(get_vertex_data(i))
    return edge


def get_child_vertex(child, vertex, vertices):
    for i in child:
        if check_is_child(i[1], vertices):
            if (
                    get_vertex_data(i[1])
                    not in all_vertex_info[get_vertex_data(vertex)]["children"]
            ):
                all_vertex_info[get_vertex_data(vertex)]["children"].append(
                    get_vertex_data(i[1])
                )

                all_vertex_info[get_vertex_data(vertex)]["args"].append(
                    {i[0]: type(i[1])}
                )
        elif is_instance_from_langchain(i[1], "langchain"):
            get_child_vertex(i[1], vertex, vertices)
        elif isinstance(i[1], list) and len(i[1]) > 2:
            for j in i[1]:
                get_child_vertex(j, vertex, vertices)


def check_is_child(child, parent):
    if child:
        for vertex in parent:
            try:
                if child == vertex:
                    return True
            except:
                if child is vertex:
                    return True
    return False


def get_children(vertices, function_list=None):
    for vertex in vertices:
        if vertex.__class__.__name__ == "AgentExecutor":
            all_agents = dir(langchain.agents)
            for j in function_list:
                if j.__name__ in all_agents:
                    parent_id = get_vertex_data(vertex)
                    children = get_function_arg_type(j, vertices)
                    if isinstance(children, list):
                        all_vertex_info[parent_id]["children"].extend(children)
                    else:
                        all_vertex_info[parent_id]["children"].append(children)
        else:
            for child in vertex:
                try:
                    if (
                            child[1] in vertices
                            and get_vertex_data(child[1])
                            not in all_vertex_info[get_vertex_data(vertex)]["children"]
                    ):
                        parent_id = get_vertex_data(vertex)
                        all_vertex_info[get_vertex_data(vertex)]["children"].append(
                            get_vertex_data(child[1])
                        )
                    elif (
                            child[1]
                            and not check_is_child(child[1], vertices)
                            and is_instance_from_langchain(child[1], "langchain")
                    ):
                        get_child_vertex(child[1], vertex, vertices)

                except:
                    if (
                            child[1]
                            and check_is_child(child[1], vertices)
                            and child[1]
                            not in all_vertex_info[get_vertex_data(vertex)]["children"]
                    ):
                        all_vertex_info[get_vertex_data(vertex)]["children"].append(
                            get_vertex_data(child[1])
                        )

                    elif (
                            child[1]
                            and not check_is_child(child[1], vertices)
                            and is_instance_from_langchain(child[1], "langchain")
                    ):
                        get_child_vertex(child[1], vertex, vertices)


def generate_random_string(length=5):
    lowercase_chars = string.ascii_lowercase + string.digits
    random_string = "".join(random.choice(lowercase_chars) for _ in range(length))
    return random_string


def get_base_class():
    id = str(uuid.uuid4())
    base_data = {
        "description": "Design Dialogues with LangFlow.",
        "name": "Modest Franklin",
        "data": {"nodes": [], "edges": [], "viewport": {"x": 1, "y": 0, "zoom": 0.5}},
        "id": id,
    }
    return base_data


def get_template(
        component_name: str, vertex_name: str, position, lc_kwargs=None, vertex=None
) -> dict | None:
    try:
        for key in all_vertex_template[component_name]:
            if key.lower() == vertex_name.lower():
                vertex_id = f"{vertex_name}_{generate_random_string()}"
                Node = {
                    "width": 0,
                    "height": 0,
                    "id": vertex_id,
                    "type": "genericNode",
                    "position": {"x": position[0], "y": position[1]},
                    "data": {"type": key, "node": {}, "id": vertex_id, "value": None},
                    "positionAbsolute": {"x": position[0], "y": position[1]},
                }
                vertex_name = key
                dict_data = all_vertex_template[component_name][key]
                for key, value in dict_data.items():
                    Node["data"]["node"][key] = value

                all_vertex_info[vertex_id] = {
                    "vertex_name": vertex_name,
                    "vertex_id": vertex_id,
                    "component_name": component_name,
                    "vertex": vertex,
                    "base_class": dict_data["base_classes"],
                    "children": [],
                    "args": [],
                }

                if lc_kwargs:
                    for key, value in lc_kwargs.items():
                        if is_instance_from_langchain(type(value), "langchain"):
                            continue

                        if key in Node["data"]["node"]["template"].keys():
                            Node["data"]["node"]["template"][key]["value"] = lc_kwargs[
                                key
                            ]

                return Node
    except:
        pass


def allocate_components(num_components):
    """Allocate the vertexes"""
    components = []
    n_nodes = 4
    shift = num_components // n_nodes
    init_x = 400
    init_y = 400
    for s in range(shift + 1):
        for i in range(n_nodes):
            angle = i * (2 * math.pi / n_nodes)
            x = (s - 1) * 30 + init_x * math.cos(math.pi - angle)
            y = init_y * math.sin(angle)
            components.append((x, y))

    return components[:num_components]


def print_vertex_and_edges(edges, all_instance, function_list1):
    vertices = []
    edge_data = []

    for i in all_instance:
        if i.__class__.__name__ == "AgentExecutor":
            all_agents = dir(langchain.agents)
            for j in function_list1:
                if j.__name__ in all_agents:
                    func_name = j.__name__.split("_")
                    func_name = "".join(func_name[1:]).title()
                    vertices.append(f"{i.__class__.__name__} ({func_name})")
        else:
            vertices.append(f"{i.__class__.__name__}")

    for edge in edges:
        edge_data.append(f"{edge['source']}-->{edge['target']}")

    # df = pd.DataFrame(data)
    # st.table(df)
    max_length = max(len(vertices), len(edge_data))
    # vertex_df = pd.DataFrame(vertices, columns=['Vertices'])
    # edge_df = pd.DataFrame(edge_data, columns=['Edge'])
    vertices += [''] * (max_length - len(vertices))
    edge_data += [''] * (max_length - len(edge_data))

    data = {
        'Vertices': vertices,
        'Edges': edge_data
    }

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame as a table
    st.table(df)
