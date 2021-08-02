import os
import subprocess
import time
from multiprocessing import Process


def run_proc(name):
    p = subprocess.Popen('ping baidu.com')
    print("子进程pid：", p.pid)


if __name__ == '__main__':
    print('父进程pid：', os.getpid())
    p = Process(target=run_proc, args=('test',))    # 必须在main中
    print('子进程将开始')
    p.start()
    # p.join()
    time.sleep(1)
    p.kill()
    print('子进程结束')
