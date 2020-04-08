def find_all_circle_paths(graph: dict, min_len=3, max_len=7):
    results = []
    nodes = list(graph.keys())
    nodes.sort()
    for i in range(min_len, max_len + 1):
        find_all_circle_path_of_length(graph, nodes, i,results)
    return results


def find_all_circle_path_of_length(graph: dict, nodes: list, length: int, results: list):
    for node in nodes[0:len(nodes) - length + 2]:
        path = [node]
        find_all_circle_path_of_length_start_with(graph, length, results, path)


def find_all_circle_path_of_length_start_with(graph: dict, length: int, results: list, path: list):
    path_len = len(path)
    last_node = path[-1]

    if last_node not in graph.keys():
        return

    if path_len == length - 1:
        for next_node in graph[last_node]:
            if next_node <= path[0]:
                continue
            if next_node in path:
                continue
            if next_node in graph.keys() and path[0] in graph[next_node]:
                results.append(path + [next_node])
    else:
        for next_node in graph[last_node]:
            if next_node <= path[0]:
                continue
            if next_node in path:
                continue
            find_all_circle_path_of_length_start_with(graph,length,results,path+[next_node])

