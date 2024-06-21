import threading
from multiprocessing import Pool, Queue, Process
import wget
import time
import os
import queue


USE_EXTERNAL_WGET = False


# 单纯的下载功能
def download_function(url, target):
    try:
        if os.path.exists(target):
            if os.path.getsize(target) > 0:
                return

        if USE_EXTERNAL_WGET:
            with open(target + '.todo', 'w') as fp:
                fp.write(url)
            os.system('wget -i "%s.todo" -O "%s"' % (target, target))
            os.remove(target + '.todo')
        else:
            wget.download(url, target)
    except Exception as ex:
        pass


# 从queue里获取下载项并下载
class DownloadWorker(threading.Thread):

    def __init__(self, todo: queue.Queue):
        threading.Thread.__init__(self)
        self.todo = todo

    def run(self):
        while True:
            item = self.todo.get()
            if item is not None:
                download_function(item[0], item[1])
            else:
                break


def download_worker(todo: Queue):
    while True:
        item = todo.get()
        download_function(item[0], item[1])
        if item is None:
            break


# 在另外线程中运行的下载管理
#class Downloader(threading.Thread):
class Downloader:

    def __init__(self, pool_size = 10):
        #threading.Thread.__init__(self)

        self.todo = queue.Queue()
        self.pool_size = pool_size

        #self.stop_after_done = False

        self.pool = []

    def start(self):
        # 启动工作进程
        for i in range(self.pool_size):
            #p = Process(target=download_worker, args=self.todo)
            #p.start()
            #self.pool[i] = p
            p = DownloadWorker(self.todo)
            p.start()
            self.pool.append(p)




    # 启动下载器
    def run(self):
        # 启动工作进程
        for i in range(self.pool_size):
            p = Process(target=download_worker, args=self.todo)
            p.start()
            self.pool[i] = p



    # 增加一个下载项目
    def add(self, url, target):
        self.todo.put((url, target))



    # 发出完成指令
    def wait_until_finish(self, track=3):
        for i in range(self.pool_size + 10):
            self.todo.put(None)

        while len(self.pool) > 0:
            print('%d items to be downloaded ...' % (self.todo.qsize() + len(self.pool)))
            time.sleep(track)
            if not self.pool[0].is_alive():
                del self.pool[0]
                track = 1




    def queue_size(self):
        return self.todo.qsize()







if __name__ == '__main__':
    pass
