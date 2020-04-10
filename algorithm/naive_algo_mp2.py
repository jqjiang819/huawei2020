'''
1. add multi_processor
'''

from tqdm import tqdm
import traceback
import sys
from common_utils.Multi_Processor2 import MultiProcessor
import common_utils.Multi_Processor2 as MP
from multiprocessing import Queue


def process_fn(process_works, output: Queue, args: list):
    #  args: [id,ctrl_pipe,min_idx,max_idx,offset,Array(request_min_idx,request_r_idx,allow_signal)]+[graph,length]
    # output: queue
    results = []
    process_id = args[0]
    ctrl_pipe = args[1]
    min_idx = args[2]
    max_idx = args[3]
    offset = args[4]
    ctrl_array = args[5]
    graph = args[-2]
    length = args[-1]
    #print("process_id {} init ,offset:{},max_idx:{},len_list:{}".format(process_id,offset,max_idx,len(process_works)))
    idx = 0
    while idx < max_idx:
        try:
            node = process_works[idx]
            path = [node]
            find_all_circle_path_of_length_start_with(graph, length, results, path)
            idx += 1
            if idx % 10 == 0 and idx != 0:
                if ctrl_array[2] == 1:
                    _left_jobs = max_idx-idx
                    if _left_jobs > 20:
                        distr_job_st_idx = _left_jobs//2 + idx
                        ctrl_pipe.put((process_id,MP.MP_DISTRIBUTE_WORKS,[distr_job_st_idx+offset,max_idx+offset]))
                        max_idx = distr_job_st_idx
                        ctrl_array[2]=0
        except Exception as e:
            print("idx:{}, min_idx:{}, max_idx:{},processId:{},length:{}".format(idx,min_idx,max_idx,process_id,len(process_works)))
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            traceback.print_tb(exc_traceback_obj)
    # print("{} finish".format(process_id))
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
    job_num = 4
    result_dict = dict()

    process_list = nodes[0:len(nodes) - length + 2]

    pipe = Queue()
    outputs = [pipe for i in range(job_num)]

    mp = MultiProcessor(process_fn=process_fn,job_num=16,works_list=process_list,args=[graph,length])
    mp.start()
    results += mp.get_result()



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

