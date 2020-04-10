from data_utils.data_loader import dataLoader1
from algorithm import naive_algo_mp2 as naive_algo
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

    def cmp_path(list1,list2):
        if len(list1) != len(list2):
            return len(list1)<len(list2)
        else:
            for i in range(len(list1)):
                if list1[i] < list2[i]:
                    return True
            return True

    #results.sort(key=lambda x:[len(x),x])

    duration = time.time()-start_tp
    correct = algo_judge.judge1(results,targets)

    print(correct)
    print("process_time: {} s".format(duration))