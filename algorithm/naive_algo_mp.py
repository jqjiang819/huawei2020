'''
1. add multi_processor
'''

from tqdm import tqdm
from common_utils.Multi_Processor import MultiProcessor
from multiprocessing import Queue


def process_fn(process_works, output: Queue, args: list):
    # args: [id(auto added),graph,length]
    # output: queue
    results = []
    process_id = args[0]
    graph = args[1]
    length = args[2]
    for node in process_works:
        path = [node]
        find_all_circle_path_of_length_start_with(graph, length, results, path)

    output.put((process_id, results))

def find_all_circle_paths(graph: dict, min_len=3, max_len=7):
    results = []
    nodes = list(graph.keys())
    nodes.sort()
    for i in range(min_len, max_len + 1):
        find_all_circle_path_of_length(graph, nodes, i,results)
    return results


def find_all_circle_path_of_length(graph: dict, nodes: list, length: int, results: list):
    # for node in tqdm(nodes[0:len(nodes) - length + 2]):
    #     path = [node]
    #     find_all_circle_path_of_length_start_with(graph, length, results, path)
    job_num = 16
    result_dict = dict()


    process_list = nodes[0:len(nodes) - length + 2]
    works_for_jobs = []
    left_num = len(process_list)
    for i in range(job_num):
        _length_for_job = left_num // (job_num+1-i)
        _works_for_job = process_list[-left_num:-left_num+_length_for_job]
        works_for_jobs.append(_works_for_job)
        left_num -= _length_for_job

    pipe = Queue()
    outputs = [pipe for i in range(job_num)]

    mp = MultiProcessor(process_fn=process_fn,job_num=16,works_for_each_job=works_for_jobs,outputs=outputs,args=[graph,length])
    mp.start()
    for i in range(job_num):
        id,_result = pipe.get()
        result_dict[id] = _result

    for i in range(job_num):
        results.extend(result_dict[i])



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

