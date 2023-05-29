import math
import os
import copy
from git import Repo
import re
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

cwd = os.getcwd()
CODE_ROOT_FOLDER = "/content/Zeeguu-API/"

REQUIREMENTS_FILE = "/content/Zeeguu-API/requirements.txt"

# If the file exists, it means we've already downloaded
if not os.path.exists(CODE_ROOT_FOLDER):
    Repo.clone_from("https://github.com/zeeguu/API", CODE_ROOT_FOLDER)


# helper function to get a file path w/o having to always provide the /content/Zeeguu-API/ prefix
def file_path(file_name):
    return CODE_ROOT_FOLDER + file_name


def ignore_requirements_txt():
    ignore_requirements_list = []
    with open(REQUIREMENTS_FILE) as file:
        for line in file:
            # ignore comments
            requirement = line.split('#')[0]  # ignore comments
            requirement = requirement.strip().lower()
            # ignore version number
            requirement = requirement.split('==')[0]
            # ignore requirements that start with 'git+'
            if requirement and not requirement.startswith('git+'):
                ignore_requirements_list.append(requirement)
    return ignore_requirements_list


# we assume that imports are always at the
# TODO for you: add full support for imports; this is not complete...
def import_from_line(line):
    # regex patterns used
    #   ^  - beginning of line
    #   \S - anything that is not space
    #   +  - at least one occurrence of previous
    #  ( ) - capture group (read more at: https://pynative.com/python-regex-capturing-groups/)
    try:
        y = re.search("^from (\S+)", line)
        if not y:
            y = re.search("^import (\S+)", line)
        return y.group(1)
    except:
        return None


# extracts all the imported modules from a file
# returns a module of the form zeeguu_core.model.bookmark, e.g.
def imports_from_file(file, ignore_list):
    all_imports = []

    lines = [line for line in open(file)]

    for line in lines:
        imp = import_from_line(line)

        if imp and imp not in ignore_list:
            all_imports.append(imp)

    return all_imports


def get_all_python_files():
    filter_list = ["test", "model", "tools", "util"]
    # root_folder = "/path/to/root/folder"

    # Walk through all the subdirectories of the root folder and find files ending with ".py"
    py_files = []
    for file in Path(CODE_ROOT_FOLDER).rglob("*.py"):
        if any(filter_item in file.name for filter_item in filter_list):
            continue  # ignore files with filter_list names
        py_files.append(str(file))

    # print(py_files)

    return py_files


def extract_imports_from_file(paths, ignore_requirements):
    imports_list = []
    for file in paths:
        imports_list.append(imports_from_file(file, ignore_requirements))
    flat_list = list(set([item for sublist in imports_list for item in sublist]))
    return flat_list


# extracting a module name from a file name
def module_name_from_file_path(full_path):
    # e.g. ../core/model/user.py -> zeeguu.core.model.user

    file_name = full_path[len(CODE_ROOT_FOLDER):]
    file_name = file_name.replace("/__init__", "")
    file_name = file_name.replace("\__init__", "")
    file_name = file_name.replace("/__main__", "")
    file_name = file_name.replace("\__main__", "")
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace("\\", ".")
    file_name = file_name.replace(".py", "")
    return file_name


def dependencies_graph(ignore_requirements):
    files = Path(CODE_ROOT_FOLDER).rglob("*.py")
    filter_list = ["test", "model", "tools", "util"]
    G = nx.Graph()

    for file in files:
        file_path = str(file)
        skip_file = False
        for filter_item in filter_list:
            if filter_item in file_path:
                skip_file = True
                break
        if skip_file:
            continue  # ignore filtered files
        module_name = module_name_from_file_path(file_path)

        if module_name.startswith('zeeguu') and module_name not in G.nodes:
            G.add_node(module_name)

        for each in imports_from_file(file_path, ignore_requirements):
            if each.startswith('zeeguu'):
                G.add_edge(module_name, each)

    return G


# a function to draw a graph
def draw_graph(G, size, name, **args):
    # calculate in-degree for each node
    in_degrees = dict(G.in_degree())

    # Get the 3 nodes with the highest in-degree
    top_5_in_degrees = sorted(in_degrees, key=lambda x: in_degrees[x], reverse=True)[:5]

    # Create a color map with red for the top 3 nodes and blue for the rest
    node_colors = []
    font_colors = []
    for node in G.nodes():
        if node in top_5_in_degrees:
            node_colors.append('red')
        else:
            node_colors.append('blue')

    # draw graph with node sizes proportional to in-degree
    pos = nx.spring_layout(G)
    plt.figure(figsize=size)
    nx.draw(G, pos, node_color=node_colors, font_size=12, font_weight='bold', with_labels=True,
            node_size=[v * 100 for v in in_degrees.values()])
    plt.savefig(name)
    # plt.show()
    plt.close()


def draw_simple_graph(G, size, name, withLayout=True):
    # draw graph with node sizes proportional to in-degree
    plt.figure(figsize=size)
    if withLayout:
        k = 5 / math.sqrt(G.order())
        pos = nx.spring_layout(G, k=k)
    nx.draw_spring(G, with_labels=True)
    # plt.show()
    plt.savefig(name + "3")
    # plt.show()
    plt.close()


def draw_graph_limited_labels(G, size, name, **args):
    # calculate in-degree for each node
    in_degrees = dict(G.in_degree())

    # Get the 3 nodes with the highest in-degree
    top_5_in_degrees = sorted(in_degrees, key=lambda x: in_degrees[x], reverse=True)[:5]

    # Create a color map with red for the top 3 nodes and blue for the rest
    node_colors = []
    font_colors = []
    labels = {}
    for node in G.nodes():
        if node in top_5_in_degrees:
            node_colors.append('red')
            labels[node] = node
        else:
            node_colors.append('blue')

    # draw graph with node sizes proportional to in-degree
    pos = nx.spring_layout(G)
    plt.figure(figsize=size)
    nx.draw(G, pos, node_color=node_colors, font_size=8, with_labels=True, font_color='white',
            node_size=[v * 100 for v in in_degrees.values()])
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', font_color='black')
    plt.savefig(name)
    # plt.show()
    plt.close()


# However, if we think a bit more about it, we realize tat a dependency graph
# is a directed graph (e.g. module A depends on m)
# with any kinds of graph either directed (nx.DiGraph) or
# non-directed (nx.Graph)

def dependencies_digraph(ignore_requirements):
    files = Path(CODE_ROOT_FOLDER).rglob("*.py")
    filter_list = ["test", "model", "tools", "util"]

    G = nx.DiGraph()
    list_of_modules = []
    for file in files:
        file_path = str(file)
        skip_file = False
        for filter_item in filter_list:
            if filter_item in file_path:
                skip_file = True
                break
        if skip_file:
            continue  # ignore filtered files
        source_module = module_name_from_file_path(file_path)

        if source_module.startswith('zeeguu') and source_module not in G.nodes:
            G.add_node(source_module)
            list_of_modules.append(source_module)

        for target_module in imports_from_file(file_path, ignore_requirements):
            if target_module.startswith('zeeguu'):
                G.add_edge(source_module, target_module)
            # print(module_name + "=>" + each + ".")

    print("=" * 30)
    print(list_of_modules)
    print("=" * 30)
    return G


def remove_singleEdges(G):
    # print(list(nx.isolates(G)))
    G.remove_nodes_from(list(nx.isolates(G)))
    return G


# extracts the parent of depth X
def top_level_package(module_name, depth=1):
    components = module_name.split(".")
    return ".".join(components[:depth])


def abstracted_to_top_level(G, depth=-1):
    aG = nx.DiGraph()
    new_copy = list(copy.deepcopy(G.nodes()))
    x = 0
    while len(new_copy) > 0:
        for item in new_copy:
            if has_depth(item, x, depth):
                if get_level_module(item, x) not in aG.nodes and get_level_module(item, x) != "":
                    if x == 0:
                        aG.add_node(get_level_module(item, x),
                                    size=calculate_total_amount_of_code(G, get_level_module_no_skip(item, x)) + 500,
                                    color="orange")
                    else:
                        aG.add_node(get_level_module(item, x),
                                    size=calculate_total_amount_of_code(G, get_level_module_no_skip(item, x)),
                                    color="lightblue")
                    if x > 0 and get_level_module(item, x - 1) != "":
                        source = get_level_module(item, x - 1)
                        destination = get_level_module(item, x)
                        if source != destination:
                            aG.add_edge(destination, source, color='black')

        newcopy2 = copy.deepcopy(new_copy)
        for item in new_copy:
            if not has_depth(item, x, depth):
                newcopy2.remove(item)
        new_copy = newcopy2
        x = x + 1

    return aG


def has_depth(module_name, current_depth, depth_cap):
    if "." in module_name:
        components = module_name.split(".")
        if depth_cap > 0:
            return len(components) - 1 >= current_depth and depth_cap >= current_depth
        else:
            return len(components) - 1 >= current_depth
    else:
        return 1 >= current_depth


def get_level_module(module_name, depth):
    components = module_name.split(".")
    if len(components) <= depth:
        return module_name
    else:
        return ".".join(components[:depth + 1])


def get_level_module_no_skip(module_name, depth):
    if "." not in module_name:
        return module_name

    components = module_name.split(".")
    result = components[0]
    for i in range(1, min(depth + 1, len(components))):
        result += "." + components[i]

    return result


def calculate_total_amount_of_code(G, currentItem):
    sizes = nx.get_node_attributes(G, "size")
    totalCode = 100
    for key, val in sizes.items():
        if key == currentItem:
            totalCode = totalCode + val

    return totalCode


def remove_nodes(G, name):
    aG = nx.DiGraph()
    for node in G.nodes():
        if node.startswith(name):
            aG.add_node(node)

    for edge in G.edges():
        source, target = edge
        if source.startswith(name) and target.startswith(name):
            aG.add_edge(source, target)
    return aG

def main():
    print(REQUIREMENTS_FILE)
    assert (file_path("zeeguu/core/model/user.py") == "/content/Zeeguu-API/zeeguu/core/model/user.py")

    assert 'zeeguu.core.model.user' == module_name_from_file_path(file_path('zeeguu/core/model/user.py'))

    # test
    print("*" * 40)
    print(ignore_requirements_txt())
    ignore_requirements = ignore_requirements_txt()
    print("*" * 40)
    print(get_all_python_files())
    print("*" * 40)
    print(extract_imports_from_file(get_all_python_files(), ignore_requirements))
    print("*" * 40)
    # Looking at the directed graph
    DG = dependencies_digraph(ignore_requirements)
    sDG = remove_singleEdges(DG)
    # Remove nodes with only one edge
    draw_graph(sDG, (40, 40), "initial", with_labels=True)
    draw_graph_limited_labels(sDG, (40, 40), "initial_limited", with_labels=True)

    for x in range(1, 6):
        ADG = abstracted_to_top_level(DG, x)
        draw_simple_graph(ADG, (60, 40), "abstract" + str(x))
        core = remove_nodes(ADG, "zeeguu.api")
        draw_simple_graph(core, (60, 40), "abstract_core" + str(x))
        api = remove_nodes(ADG, "zeeguu.core.model")
        # draw_simple_graph(api, (60, 40), "abstract.core.model" + str(x), False)
        draw_simple_graph(api, (30, 20), "abstract_core_model" + str(x), False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
