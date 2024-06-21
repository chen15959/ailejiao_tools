import json
import io
import os
import os.path
from time import sleep

from myhttp import prepare, get, download, APP_SERVER, post
import shutil
from config import Config
import threading

import wget


CLASS_CIRCLE_PAGE_SIZE = 10
#SAVE_PATH = 'c:\\temp\\0621\\'


def getname(time, user):
    time = time.replace(' ', '_').replace(':', '-')
    return "%s@%s" % (time, user)

def valid(item):
    if item is not None:
        return len(str(item)) > 0

    return False


class PictureDownloader(threading.Thread):

    def __init__(self, path):
        threading.Thread.__init__(self)
        self.todo = []
        self.path = path

    def add(self, url, id):
        ext = str(url).split('?')[0].split('.')[-1]
        target = '%d.%s' % (id, ext)
        self.todo.append((url, os.path.join(self.path, target)))

    def run(self):
        try:
            for item in self.todo:
                wget.download(item[0], item[1])
        except Exception as ex:
            pass



def save_class_circle(item):
    id = item['id']
    name = getname(item['createTime'], item['createUserName'])
    #"%s@%s" % (time, user)

    datadir = os.path.join(Config().get('download_folder'), name)
    if os.access(datadir, os.F_OK):
        return False;

    print('\tsave class circle %s' % name)
    os.mkdir(datadir)

    # 保存文字
    if valid(item['content']):
        with open(os.path.join(datadir, 'content.txt'), 'w', encoding='utf8') as fp:
            text = item['content']
            fp.write(text)

    # 保存回复
    if len(item['comments']) > 0:
        for item1 in item['comments']:
            if valid(item1['comment']):
                name = 'comment_%s.txt' % getname(item1['createTime'], item1['createUserName'])
                with open(os.path.join(datadir, name), 'w', encoding='utf8') as fp:
                    fp.write(item1['comment'])

    # 下载图片
    pd = PictureDownloader(datadir)
    for picture in item['ossResources']:
        pd.add(picture['url'], picture['id'])

    pd.start()







def download_class_circle(start=1,stop=100000):
    page = start
    has_next = True
    while has_next and page <= stop:
        print("downloading page %d ..." % page, end='')
        # 班级圈分页下载
        r = get(APP_SERVER + "/class_circle_messages/?currentPage=%d&pageSize=%d&platform=app" % (page, CLASS_CIRCLE_PAGE_SIZE))

        # 本地保存一下json存档
        with open(os.path.join(Config().get('download_folder'), 'class_circle_page_%d.json' % page), 'w', encoding='utf8') as fp:
            json.dump(r, fp)

        items = r['items']
        print(' %d items downloaded.' % len(items))
        # 是否有下一页
        has_next = (len(items) >= CLASS_CIRCLE_PAGE_SIZE) #or r['isMore'] > 0
        page = page + 1

        # 处理每一个班级圈项目
        for item in items:
            save_class_circle(item)

    # 等待所有异步下载完成
    print('wait...')
    while (threading.activeCount() > 1):
        sleep(1)

    print('all done.')


if __name__ == '__main__':
    prepare()

    download_class_circle(3,3)


