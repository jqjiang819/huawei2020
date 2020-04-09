from data_utils.data_loader import dataLoader1
from algorithm import naive_algo_mp as naive_algo
from common_utils import algo_judge
import time

graph_file_path = "./test_data/1004812/test_data.txt"
results_file_path = "./test_data/1004812/result.txt"

if __name__ == "__main__":
    start_tp = time.time()
    dataloader = dataLoader1(graph_file_path=graph_file_path,test_file_path=results_file_path)
    graph = dataloader.get_graph()
    targets = dataloader.get_results()

    results = naive_algo.find_all_circle_paths(graph)
    duration = time.time()-start_tp
    correct = algo_judge.judge1(results,targets)

    print(correct)
    print("process_time: {} s".format(duration))