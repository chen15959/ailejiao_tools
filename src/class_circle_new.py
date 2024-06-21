import json
import os
import os.path
from time import sleep

from myhttp import prepare, get, download, APP_SERVER, post
import shutil
from config import Config
import threading

import wget

from downloader import Downloader


CLASS_CIRCLE_PAGE_SIZE = 10
USE_EXTERNAL_WGET = True


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
            print('ClassCircle    %d                     %s' % (class_circle.id, class_circle.time))
            class_circle.save()



if __name__ == '__main__':
    prepare()

    downloader.start()

    download_class_circle(1,1)

    # 等待所有异步下载完成
    downloader.wait_until_finish()

    print('all done.')

