from data_utils.data_loader import dataLoader1
from algorithm import naive_algo
from common_utils import algo_judge

graph_file_path = "./test_data/test_data.txt"
results_file_path = "./test_data/result.txt"

dataloader = dataLoader1(graph_file_path=graph_file_path,test_file_path=results_file_path)
graph = dataloader.get_graph()
targets = dataloader.get_results()

results = naive_algo.find_all_circle_paths(graph)

correct = algo_judge.judge1(results,targets)

print(correct)