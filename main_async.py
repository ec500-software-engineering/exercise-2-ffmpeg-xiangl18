import subprocess
import queue
import asyncio
import shutil
import time


CMD = 'ffmpeg -y -i {input} -b:v {bit_rate}M -r {fps} -s hd{res} {output}'
FFMPEG = shutil.which('ffmpeg')
Ntask = 2

# input video and output videos forms
input_list = [{'input': 'video.avi', 'output': 'outputVideo480p.mp4', 'rate': '1', 'fps': '60', 'res': '480'},
              {'input': 'video.avi', 'output': 'outputVideo720p.mp4', 'rate': '1', 'fps': '60', 'res': '720'}]

# check if there is ffmpeg in the environment
if not FFMPEG:
    raise FileNotFoundError('FFMPEG not found')


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


async def ffmpeg(task_queue: asyncio.Queue, task_id: asyncio.Queue):
    """
    function to process video using queue.
    """
    assert isinstance(FFMPEG, str)
    while not task_queue.empty():
        try:
            task = await task_queue.get()
            process_id = await task_id.get()
            cmd = process_input(task['input'], task['output'], task['rate'], task['fps'], task['res'])
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('=' * 20 + ' process {}: Converting file {} to output file {} '
                  .format(process_id, task['input'], task['output']) + '=' * 20)
            proc.communicate()
            ret = proc.returncode
            if ret != 0:
                print(
                    '=' * 20 + ' process {}: Failed to converting file {} | return code {} '
                    .format(process_id, task['input'], ret) + '=' * 20)
            else:
                print('=' * 20 + ' process {}: Completed converting file {} '
                      .format(process_id, task['input']) + '=' * 20)
                print(' Done ')
            task_queue.task_done()
            task_id.task_done()
        except queue.Empty:
            print("no task")
            pass


async def run(task_list):
    """
    main function to run the whole process.
    """
    # this code is for multi process based on the cpu logical cores, so far the number of tasks is locked to 2.
    # Ntask = os.cpu_count()  # includes logical cores
    # if not isinstance(Ntask, int):
    #     Ntask = 2
    
    task_queue = asyncio.Queue()
    tasks = []
    task_id = asyncio.Queue()
    for f, i in zip(task_list, range(Ntask)):
        await task_queue.put(f)
        await task_id.put(i)
        tasks.append(asyncio.ensure_future(ffmpeg(task_queue, task_id)))
    await task_queue.join()
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(input_list))
    loop.stop()
    end = time.time()
    print('running time:', end)
