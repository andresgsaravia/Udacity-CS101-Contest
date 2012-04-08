# This code is provided under a CC BY-NC-SA license
# see http://creativecommons.org/licenses/by-nc-sa/3.0/ for more details
# 
# Andres Garcia Saravia Ortiz de Montellano
# ags3006@gmail.com
# April 8th, 2012

from search_engine import *

# How many letter will have the printed link in each node
name_length = 33


def biggest_rank(ranks):
    big = 0.0
    for entry in ranks:
        if ranks[entry] > big:
            big = ranks[entry]
    return big


font_size_multiplier = 10 # increse / decrease to have bigger/smaller fonts and arrows


def node_name(string):
    return '"' + string + '"'


def node_label(string):
    if len(string) > name_length:
        return string[:(name_length - 3) / 2] + '...' + string [-(name_length - 3) / 2:]
    else:
        return string


def node_dot(node, ranks):
    result = node_name(node) 
    result += ' [label="' + node_label(node) + '\\n' + str("%.4f" % ranks[node]) + '"' 
    result += ', fontsize=' + str(ranks[node] * font_size_multiplier  / biggest_rank(ranks))
    result += ', penwidth=' + str(ranks[node] * font_size_multiplier  / (biggest_rank(ranks) * 10)) 
    result += ', URL=' + node_name(node) 
    result += '];'
    return result


def edge_dot(source, target, ranks, name = ''):
    sr = node_name(source)
    tg = node_name(target)
    dot_string = sr + ' -> ' + tg 
    dot_string += ' ['
    dot_string += 'penwidth=' + str(ranks[source] * font_size_multiplier  / (biggest_rank(ranks) * 10))
    dot_string += ', arrowsize=' + str(ranks[source] * font_size_multiplier / (biggest_rank(ranks) * 10))
    if len(name) > 0:
        dot_string += ', label="' + name + '"'
    dot_string += '];'
    return dot_string


def all_nodes_dot(graph, ranks):
    dot_string = ''
    for node in graph:
        dot_string += node_dot(node, ranks) + '\n'
    return dot_string


def all_edges_dot(graph, ranks):
    dot_string = ''
    for source in graph:
        for target in graph[source]:
            dot_string += edge_dot(source, target, ranks) + '\n'
    return dot_string


def graph_dot(graph, ranks):
    dot_string = 'digraph G {\n'
    dot_string += all_nodes_dot(graph, ranks) + all_edges_dot(graph, ranks)
    dot_string += '}'
    return dot_string

# Makes a simple "lucky_search" of "keyword" in "index" and returns a graph with links 
# into and out from the result; "graph" is the one returned by "crawl_web"
def lookup_graph(index, ranks, keyword, graph):
    lucky = lucky_search(index, ranks, keyword)
    result_graph = {}
    result_graph[lucky] = graph[lucky]
    for page in graph:
        if lucky in graph[page]:
            result_graph[page] = [lucky]
    for page in result_graph[lucky]:
        if not page in result_graph:
            result_graph[page] = []
    return result_graph
    

def write_dot_file(filename, graph, ranks):
    f = open(filename, "w")
    f.write(graph_dot(graph, ranks))
    f.close()


def write_dot_lookup(filename, index, ranks, keyword, graph):
    g = lookup_graph(index, ranks, keyword, graph)
    write_dot_file(filename, g, ranks)
