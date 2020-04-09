from multiprocessing import Process
import os


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
            self.process_fn(self.process_file, self.output_dir, self.args)


class MultiProcessor():
    def __init__(self, process_fn=None, job_num=1, works_for_each_job:list=None, outputs:list=None,args:list = []):
        self.jobs_list = []
        self.jobs_num = job_num
        self.works_for_each_job = works_for_each_job
        self.process_fn = process_fn
        self.output_dirs = outputs
        self.args = args
        self._init_jobs()


    def _init_jobs(self):

        if self.works_for_each_job == None:
            self.works_for_each_job = [None] * self.jobs_num
        else:
            assert type(self.works_for_each_job) == list, "files_for_each_job only support type < List > Now"
            assert len(self.works_for_each_job) == self.jobs_num, "length of files_for_each_job not equals to job_num"

        if self.output_dirs == None:
            self.output_dirs = [None] * self.jobs_num
        else:
            assert type(self.output_dirs) in [str, list], "output_dirs not str nor list"
            if type(self.output_dirs) == str:
                self.output_dirs = [self.output_dirs for i in range(self.jobs_num)]

        for i in range(self.jobs_num):
            self.jobs_list.append(
                ProcessUnit(process_file_list=self.works_for_each_job[i], output_dir=self.output_dirs[i],
                            process_fn=self.process_fn, args=[i]+self.args))

    def start(self):
        for unit in self.jobs_list:
            unit.start()


if __name__ == '__main__':
    import time
    CONST = 'const'

    def process_fn(process_list, output_dir, args=None):
        for i in range(20):
            print('\r num: {} from unit id: {},const:{}'.format(i, args[0],CONST), end='')
            time.sleep(0.2)


    multi_processor = MultiProcessor(job_num=4, process_fn=process_fn)
    multi_processor.start()
