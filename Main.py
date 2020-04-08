
DATA_PATH = "data/test_data.txt"


class Node:
    instances = {}

    def __new__(cls, id, *args, **kwargs):
        if id not in cls.instances:
            cls.instances[id] = object.__new__(cls)
        return cls.instances[id]

    def __init__(self, id, tid=0, give=0):
        if "id" not in self.__dict__:
            self.id = id
            self.amount = 0
            self.children = []
        if tid != 0:
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
    pass


def dfs_step(node, stack, visited, results):
    pass


def start():
    read_data(DATA_PATH)
    print(len(Node.instances))


if __name__ == "__main__":
    start()
