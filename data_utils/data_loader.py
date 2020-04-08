class dataLoader1():
    def __init__(self,graph_file_path=None,test_file_path=None):
        if graph_file_path is not None:
            self.load_graph_file(graph_file_path)
        if test_file_path is not None:
            self.load_result_file(test_file_path)

    def load_graph_file(self,graph_file_path):
        self.graph = dict()
        with open(graph_file_path,'r',encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                id1,id2,val = line.strip().split(',')
                vertex_set = self.graph.setdefault(int(id1),set())
                vertex_set.add(int(id2))

    def load_result_file(self,test_file_path):
        self.result = []
        with open(test_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines[1:]:
                path = line.strip().split(',')
                path = [int(_id) for _id in path]
                self.result.append(path)

    def get_graph(self):
        return self.graph

    def get_results(self):
        return self.result