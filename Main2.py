import os
import time
import tqdm
import functools

from collections import defaultdict

import CheckResult

DATA_PATH = "data/1004812/test_data.txt"
TEST_PATH = "data/1004812/result.txt"
OUTPUT_PATH = "output/results.txt"


def load_data(path):
    graph = defaultdict(list)
    graph_r = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for l in f.readlines():
            l = l.strip()
            if l == "":
                continue
            fr, to, am = l.split(",")
            graph[int(fr)].append(int(to))
            graph_r[int(to)].append(int(fr))
    for c in graph.values():
        c.sort()
    for c in graph_r.values():
        c.sort()
    return graph, graph_r


def dfs(graph, graph_r):
    results = []
    cache = {}
    visited = {k:0 for k in graph.keys()}
    for node in tqdm.tqdm(sorted(graph.keys())):
        prune(graph, node, node, 0, visited, cache)
        prune(graph_r, node, node, 0, visited, cache)
        dfs_step(graph, node, [], visited, cache, results)
    return results


def dfs_step(graph, node, path, visited, cache, results):
    visited[node] = 1
    path.append(node)
    for child in graph[node]:
        if child == path[0]:
            if len(path) > 2:
                results.append(tuple(path))
            continue
        if child < path[0] or visited.get(child, 0) == 1 or cache.get(child, -1) != path[0]:
            continue
        if len(path) < 7:
            dfs_step(graph, child, path, visited, cache, results)
    visited[node] = 0
    path.pop(-1)


def prune(graph, node, start, depth, visited, cache):
    visited[node] = 1
    # path.append(node)
    depth += 1
    for child in graph[node]:
        if child < start or visited.get(child, 0) == 1:
            continue
        cache[child] = start
        if depth < 3:
            prune(graph, child, start, depth, visited, cache)
    visited[node] = 0
    # path.pop(-1)
    depth -= 1


def start():
    g, g_r = load_data(DATA_PATH)
    results = dfs(g, g_r)
    results.sort(key=lambda x: len(x))
    return results


if __name__ == "__main__":
    t0 = time.time()
    results = start()
    print(f"iteration in {time.time() - t0} s")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("{0}\n".format(len(results)))
        for r in results:
            f.write("{0}\n".format(','.join(map(str, r))))
    print(f"finished in {time.time() - t0} s")
    print(f"results check:", CheckResult.check(TEST_PATH, OUTPUT_PATH))
    
