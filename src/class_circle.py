import json
import io
import os
import os.path
from myhttp import prepare, get, download, APP_SERVER, post
import shutil
from config import Config




def process_picture(folder, ccid, jo):
    id = jo['id']
    fnp = jo['fileName'].split('.')
    type = fnp[len(fnp) - 1]

    print("\tdownload picture %d-%d ..." % (ccid, id), end='')

    if True:
        try:
            jo1 = get('%s/class_circle_messages/%d/oss_resources/%d/origin_resource?platform=app' % (APP_SERVER, ccid, id))

            if Config().debug:
                with open(os.path.join(folder, '%d.json' % id), 'w') as fp:
                    json.dump(jo1, fp)

            download(jo1['ossResourceUrl'], os.path.join(folder, "%d.%s" % (id, type)))
        except:
            download(jo['url'], os.path.join(folder, "%d_normal.%s" % (id, type)))
    else:
        print("ccid=%d, pid=%d" % (ccid, id))

    print(' done')


def process_class_circle(folder, jo):
    id = jo['id']
    time = jo['createTime'].replace(' ', '_').replace(':', '-')
    name = "%d_%s" % (id, time)

    print('process class circle [%d] (%s)' % (id, time))

    datadir = os.path.join(folder, name)
    if os.access(datadir, os.F_OK):
        #TODO 是否会存在内容被zQWTY4
        print('already done')
        return False;
    else:
        tempdir = os.path.join(folder, str(id))
        if os.access(tempdir, os.F_OK):
            shutil.rmtree(tempdir)
            #os.rmdir(tempdir)

        os.mkdir(tempdir)

        # 下载图片
        for picture in jo['ossResources']:
            process_picture(tempdir, id, picture)

        # 下载文字
        with open(os.path.join(tempdir, 'content.txt'), 'w', encoding='utf8') as fp:
            text = jo['content']
            fp.write(text)


        os.rename(tempdir, datadir)

        print('class circle [%d] done' % id)



def praise_class_circle(jo):
    for comment in jo['comments']:
        if str(comment['createUserId']) == Config().get('userid'):
            return

    ccid = jo['id']
    print('praise class circle [%d] (%s) ...' % (ccid, jo['createTime']), end='')

    url = APP_SERVER + '/class_circle_messages/%d/comments?objJsonStr=#7B#22createUserId#22#3A%s#2c#22isPraised#22#3Atrue#7D&platform=app' % (ccid, Config().get('userid'))
    url = url.replace('#', '%')

    post(url, data='')
    #print(url)

    print(' done')



if __name__ == '__main__':
    items = []
#    login('13761240204', '123')
#    r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
#    items = r['item']
    Config().load('config.ini')

    with open('test/banjiquan.json', 'r', encoding='utf8') as fp:
        j = json.load(fp)
        for item in j['data']['items']:
            #process_class_circle("test/", item)
            praise_class_circle(item)







