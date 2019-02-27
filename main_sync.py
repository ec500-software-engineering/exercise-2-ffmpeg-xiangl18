import shutil
import subprocess
import threading
import queue
import time


CMD = 'ffmpeg -y -i {input} -b:v {bit_rate}M -r {fps} -s hd{res} {output}'
FFMPEG = shutil.which('ffmpeg')
if not FFMPEG:
    raise FileNotFoundError('FFMPEG not found')
Ntask = 2


class ffmpeg(threading.Thread):
    """
    thread to process input videos.
    """
    def __init__(self, task_queue, process_id):
        super().__init__()
        self.queue = task_queue
        self.worker_id = process_id

    def run(self):
        while 1:
            try:
                info_dict = self.queue.get(block=False)
                if info_dict is not None:
                    if 'exit' in info_dict:
                        print('work is done')
                        break
                    else:
                        print('='*20 + ' process {}: Converting file {} to output file {} '
                              .format(self.worker_id, info_dict['input'], info_dict['output']) + '='*20)

                        cmd = process_input(info_dict['input'], info_dict['output'],
                                            info_dict['rate'], info_dict['fps'], info_dict['res'])
                        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        process.communicate()
                        ret = process.returncode
                        if ret != 0:
                            print(
                                '='*20 + ' process {}: Failed to converting file {} | return code {} '.format(
                                    self.worker_id, info_dict['input'], ret) + '='*20)
                        else:
                            print('='*20 + ' process {}: Completed converting file {} '.format(
                                    self.worker_id, info_dict['input']) + '='*20)
                self.queue.task_done()
            except queue.Empty:
                print("no task")
                pass


def process_input(input_filename, output_filename, bit_rate, fps, res):
    """
    function to process input video format.
    """
    cmd = CMD.format(
        input=input_filename,
        bit_rate=bit_rate,
        fps=fps,
        res=res,
        output=output_filename)
    return cmd


def main():
    """
    main function to run the whole process.
    """
    thread_list = []
    task_queue = queue.Queue()
    # Ntask = os.cpu_count()  # includes logical cores
    # if not isinstance(Ntask, int):
    #     Ntask = 2
    task_list = [{'input': 'video.avi', 'output': 'outputVideo_480p.mp4', 'rate': '60', 'fps': '1', 'res': '480'},
                 {'input': 'video.avi', 'output': 'outputVideo1_720.mp4', 'rate': '60', 'fps': '1', 'res': '720'}]
    for task in task_list:
        task_queue.put(task)
    for i in range(Ntask):
        task_queue.put({'exit': 0})
    for i in range(Ntask):
        thread_list.append(ffmpeg(task_queue, i))
    print('Start {} process......'.format(Ntask))
    for i in range(Ntask):
        thread_list[i].start()
    for i in range(Ntask):
        thread_list[i].join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('running time:', end)
