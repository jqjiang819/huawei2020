from multiprocessing import Process,Array,Semaphore,Queue
import os

"""
control format: (id,command,args)
process_fn: args: [id,ctrl_pipe,min_idx,max_idx,offset,Array(request_min_idx,request_r_idx,allow_signal)] output: output_pipe
output_format: (id,result)
"""

MP_CTRL_FINISH = 1 # when process finish
# MP_ALLOW_DISTRIBUTE_WORKS = 2 # when controller allow process to distribute work, this handled by process_fn logic
# MP_NO_ALLOW_DISTRIBUTE_WORKS = 3 # same as MP_ALLOW_DISTRIBUTE_WORKS
MP_DISTRIBUTE_WORKS = 4 # args: min_idx,max_idx



class ProcessUnit(Process):
    def __init__(self, process_file_list=None, process_fn=None, output_dir=None, args:list=[0]):
        super(ProcessUnit, self).__init__()
        self.process_file = process_file_list
        self.process_fn = process_fn
        self.output_dir = output_dir
        self.id = args[0]
        self.args = args

    def run(self) -> None:
        if self.process_fn == None:
            return
        else:
            try:
                self.process_fn(self.process_file, self.output_dir, self.args)
                ctrl_pipe = self.args[1]
                ctrl_pipe.put((self.id,MP_CTRL_FINISH,None))
            except:
                ctrl_pipe = self.args[1]
                ctrl_pipe.put((self.id, MP_CTRL_FINISH, None))


class MultiProcessor():
    def __init__(self, process_fn=None, job_num=1, works_list:list=None,args = []):
        self.jobs_list = []
        self.jobs_num = job_num
        self.left_jobs = job_num
        self.result_tree = self.ResultTree()
        self.works_list = works_list
        self.process_fn = process_fn
        self.left_resources = job_num
        self.ctrl_pipe = Queue()
        self.result_pipe = Queue()
        self.worker_status = dict()  # id: [treeNode, array]
        self.job_queue = self.JobQueue()
        self.args = args
        self._init_jobs()


    class JobQueue():
        def __init__(self):
            self.queue = []
        def length(self):
            return len(self.queue)

        def dequeue(self):
            if self.length() > 0:
                return self.queue.pop(0)

        def enqueue(self,_id):
            self.queue.append(_id)

        def remove(self,_id):
            for i in range(self.length()):
                if self.queue[i] == _id:
                    self.queue.pop(i)
                    return _id
            return None

        def remove_to_last(self,_id):
            removed = self.remove(_id)
            if removed != None:
                self.enqueue(_id)

    class ResultTree():
        class TreeNode():
            def __init__(self):
                self._vals = []
                self.next = []

        def __init__(self,init_num:int = 0):
            self.head = self.init_tree(init_num)

        def init_tree(self,init_num=1):
            self.head = self.TreeNode()
            _next = []
            for i in range(init_num):
                _next.append(self.TreeNode())
            self.head.next = _next
            return self.head

        def get_result(self):
            result = self.traverseTree(self.head)
            return result

        def traverseTree(self,treeNode:TreeNode):
            result = []+treeNode._vals
            for ch_node in treeNode.next:
                result += self.traverseTree(ch_node)
            return result

        def add_node(self,prtNode:TreeNode,on_back = True):
            c_node = self.TreeNode()
            if on_back:
                prtNode.next.append(c_node)
            else:
                prtNode.next.insert(0,c_node)
            return c_node

    def _init_jobs(self):

        if self.works_list == None:
            return

        left_num = len(self.works_list)
        offset = 0
        for i in range(self.jobs_num):
            self.max_id = i
            _length_for_job =left_num  // (self.jobs_num - i)
            _works_for_job = []
            if i < (self.jobs_num - 1):
                _works_for_job = self.works_list[-left_num:-left_num + _length_for_job]
            else:
                _works_for_job = self.works_list[-left_num:]
            left_num -= _length_for_job

            # args: [id, ctrl_pipe, min_idx, max_idx, offset, Array(request_min_idx, request_r_idx, allow_signal)]
            _array = Array('i',3)
            _node = self.result_tree.add_node(self.result_tree.head)
            self.jobs_list.append(
                ProcessUnit(process_file_list=_works_for_job, output_dir=self.result_pipe,
                            process_fn=self.process_fn, args=[i,self.ctrl_pipe,0,_length_for_job,offset,_array]+self.args))
            offset += _length_for_job
            #print("gen jobs {}  work {}({})-{}({}),job_queue:{},offset:{}".format(i,len(self.works_list)-left_num,
                                                                                 # _works_for_job[0], len(self.works_list)-left_num+_length_for_job,
                                                                                 # _works_for_job[-1],
                                                                                 # self.job_queue.queue,offset))
            self.job_queue.enqueue(i)
            self.worker_status[self.max_id] = [_node,_array]


    def start(self):
        for unit in self.jobs_list:
            unit.start()
            self.left_jobs -= 1

        while self.left_jobs < self.jobs_num:

            process_id,command,args = self.ctrl_pipe.get()
            if command == MP_CTRL_FINISH:
                #print("receive {} finished,job_queue:{}".format(process_id,self.job_queue.queue))
                #print("left_jobs:{}".format(self.left_jobs))
                result_process_id,result = self.result_pipe.get()
                _node = self.worker_status[result_process_id][0]
                _node._vals += result
                self.left_jobs += 1 + self.worker_status[process_id][1][2] # allow_distribute_signal
                self.job_queue.remove(process_id)
                #print("remove:{},job_queue:{}".format(process_id,self.job_queue.queue))


                for enqueue_jobs_id in self.job_queue.queue:
                    if self.left_jobs == 0:
                        break
                    _job_array = self.worker_status[enqueue_jobs_id][1]
                    if (_job_array[2] == 0):
                        self.left_jobs -= 1
                        _job_array[2] = 1


            elif command == MP_DISTRIBUTE_WORKS:
                #command_args: min_idx,max_idx
                # process_args: [id, ctrl_pipe, min_idx, max_idx, offset, Array(request_min_idx, request_r_idx, allow_signal)]
                #print("receive {} distribute work {}({})-{}({}),job_queue:{}".format(process_id,args[0],self.works_list[args[0]],args[1],self.works_list[args[1]-1],self.job_queue.queue))
                self.max_id += 1
                _array = Array('i', 3)
                _node = self.result_tree.add_node(self.worker_status[process_id][0],on_back=False)
                _works_for_job = self.works_list[args[0]:args[1]]
                #print("distribute process_id:{} ".format(self.max_id))
                self.jobs_list.append(
                    ProcessUnit(process_file_list=_works_for_job, output_dir=self.result_pipe,
                                process_fn=self.process_fn,
                                args=[self.max_id, self.ctrl_pipe, 0, args[1]-args[0], args[0], _array]+self.args))

                self.job_queue.enqueue(self.max_id)
                self.worker_status[self.max_id] = [_node, _array]
                # remove distributed task to last
                self.job_queue.remove(process_id)

                self.job_queue.enqueue(process_id)
                self.jobs_list[-1].start()

    def get_result(self):
        return self.result_tree.get_result()
import time
CONST = 'const'
def _test_process_fn(process_list, output_dir, args=None):
    for i in range(5):
        print('\r num: {} from unit id: {},const:{}'.format(i, args[0],CONST), end='')
        time.sleep(0.2)
    output_dir.put((args[0],""))

if __name__ == '__main__':

    multi_processor = MultiProcessor(job_num=1, process_fn=_test_process_fn,works_list=list(range(20)))
    multi_processor.start()
