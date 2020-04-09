import os
import time
import tqdm
import functools

import CheckResult


DATA_PATH = "data/54/test_data.txt"
TEST_PATH = "data/54/result.txt"
OUTPUT_PATH = "output/results.txt"


class Node:
    instances = {}

    def __new__(cls, id, *args, **kwargs):
        if id not in cls.instances:
            cls.instances[id] = object.__new__(cls)
        return cls.instances[id]

    def __init__(self, id, tid=-1, give=0):
        if "id" not in self.__dict__:
            self.id = id
            self.amount = 0
            self.children = []
        if tid != -1:
            self.add_child(tid, give)

    def add_child(self, tid, give):
        target = Node(tid)
        target.amount += give
        self.amount -= give
        self.children.append(target)


def read_data(path):
    with open(path, "r") as f:
        for l in f.readlines():
            l = l.strip()
            if l == "":
                continue
            fr, to, am = l.split(",")
            Node(int(fr), int(to), int(am))


def dfs(nodes):
    stack = []
    visited = {}
    results = []
    for n in tqdm.tqdm(nodes):
        if not visited.get(n, False):
            dfs_step(n, stack, visited, results)
    return results


def dfs_step(node, stack, visited, results):
    if len(stack) > 6:
        return
    stack.append(node)
    visited[node.id] = True
    for child in node.children:
        if child in stack:
            r = stack[stack.index(child):]
            if len(r) > 2:
                results.append(r)
        elif not visited.get(child.id, False):
            dfs_step(child, stack, visited, results)
    visited[node.id] = False
    stack.pop(-1)


def res_cmp(x, y):
    if len(x) != len(y):
        return len(x) - len(y)
    else:
        return 1 if x > y else -1


def make_results(results):
    out = []
    for r in set(map(tuple, results)):
        # extract id
        rid = list(map(lambda x: x.id, r))
        min_idx = rid.index(min(rid))
        out.append(tuple(rid[min_idx:]+rid[:min_idx]))
    return list(set(out))


def start():
    read_data(DATA_PATH)
    results = make_results(dfs(Node.instances.values()))
    results.sort(key=functools.cmp_to_key(res_cmp))
    return results


if __name__ == "__main__":
    t0 = time.time()
    results = start()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("{0}\n".format(len(results)))
        for r in results:
            f.write("{0}\n".format(','.join(map(str, r))))
    print(f"finished in {time.time() - t0} s")
    print(f"results check:", CheckResult.check(TEST_PATH, OUTPUT_PATH))
