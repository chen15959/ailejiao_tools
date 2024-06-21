import json
import io
import os
import os.path
from time import sleep

from PIL import Image

from myhttp import prepare, get, download, APP_SERVER, post
import shutil
from config import Config
import threading

import wget
import PIL

from downloader import Downloader


CLASS_CIRCLE_PAGE_SIZE = 20
USE_EXTERNAL_WGET = True
#SAVE_PATH = 'c:\\temp\\0621\\'


downloader = Downloader()


def gettime(time):
    return time.replace(' ', '_').replace(':', '-')

def getname(time, user):
    return "%s@%s" % (gettime(time), user)

def valid(item):
    if item is not None:
        return len(str(item)) > 0

    return False


class ClassCircle:

    def __init__(self, jsonObj):
        self.json = jsonObj

        self.id = jsonObj['id']
        self.time = gettime(jsonObj['createTime'])
        #self.path = os.path.join(Config().get('download_folder'), self.time)
        self.user = jsonObj['createUserName']



    def save(self):

        path = os.path.join(Config().get('download_folder'), self.time)

        if not os.access(path, os.F_OK):
            os.mkdir(path)

        # 保存文字
        if valid(self.json['content']):
            with open(os.path.join(path, 'content_by_%s.txt' % self.user), 'w', encoding='utf8') as fp:
                text = self.json['content']
                fp.write(text)

        # 保存回复
        if len(self.json['comments']) > 0:
            for item in self.json['comments']:
                if valid(item['comment']):
                    name = 'comment_at_%s_by_%s.txt' % (gettime(item['createTime']), item['createUserName'])
                    with open(os.path.join(path, name), 'w', encoding='utf8') as fp:
                        fp.write(item['comment'])

        # 处理资源
        print("RESOURCE: %s|" % ('>'* len(self.json['ossResources'])))
        print("          ", end='')

        for resource in self.json['ossResources']:
            url = resource['url']

            try:
                r = get((APP_SERVER + '/class_circle_messages/%d/oss_resources/%d/origin_resource?platform=app') % (self.id, resource['id']))
                url = r['ossResourceUrl']
            except Exception as ex:
                pass

            ext = str(url).split('?')[0].split('.')[-1]
            downloader.add(url, os.path.join(path, '%d.%s' % (resource['id'], ext)))
            print('>', end='')

        print('| done.')






class PictureDownloader(threading.Thread):

    def __init__(self, path):
        threading.Thread.__init__(self)
        self.todo = []
        self.path = path

    def add(self, url, id):
        ext = str(url).split('?')[0].split('.')[-1]
        target = '%d.%s' % (id, ext)
        self.todo.append((url, target))

    def run(self):
        for item in self.todo:
            try:
                target = os.path.join(self.path, item[1])
                if os.path.exists(target):
                    if os.path.getsize(target) > 0:
                        target = None
                # with open(target, 'rb') as fp:
                #     im = Image.open(fp)
                #     try:
                #         im.verify()
                #         target = None
                #     except:
                #         im.close()
                #         fp.close()
                #         os.remove(target)

                if target is not None:
                    if USE_EXTERNAL_WGET:
                        with open(target + '.todo', 'w') as fp:
                            fp.write(item[0])
                        os.chdir(self.path)
                        os.system('wget -i %s.todo -O "%s"' % (item[1], item[1]))
                        os.remove(target + '.todo')
                    else:
                        wget.download(item[0], target)
            except Exception as ex:
                pass



def save_class_circle(item):
    id = item['id']
    name = getname(item['createTime'], item['createUserName'])
    #"%s@%s" % (time, user)

    datadir = os.path.join(Config().get('download_folder'), name)

    print('\tsave class circle %s' % name)
    if not os.access(datadir, os.F_OK):
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
            class_circle = ClassCircle(item)
            print('ClassCircle    %d -> %s' % (class_circle.id, class_circle.time))
            class_circle.save()



if __name__ == '__main__':
    prepare()

    downloader.start()

    download_class_circle(1,1)

    # 等待所有异步下载完成
    downloader.wait_until_finish()
    #while downloader.is_alive():
    #    print('%d files to download...' % downloader.queue_size())
    #    sleep(2)

    print('all done.')

