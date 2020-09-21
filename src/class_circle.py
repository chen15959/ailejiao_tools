import json
import io
import os
import os.path
from myhttp import prepare, get, download, APP_SERVER
import shutil


# class ClassCirclePicture(object):
#     _id = -1
#     _cc = -1
#     _thumbnail = ''
#     _normal = ''
#     _original = ''
#     _type = ''
#
#     def __init__(self, jo, ccid):
#         self._cc = ccid
#         self._id = jo['id']
#         self._thumbnail = jo['thumbnailUrl']
#         self._normal = jo['url']
#         fnp = jo['fileName'].split('.')
#         self._type = fnp[len(fnp) - 1]
#
#     def download(self, folder):
#         try:
#             jo = get('%s/class_circle_messages/%d/oss_resources/%d/origin_resource?platform=app' % (APP_SERVER, self._cc, self._id))
#             download(jo['ossResourceUrl'], os.path.join(folder, "%d_original.%s" % (self._id, self._type)))
#         except:
#             try:
#                 download(self._normal, os.path.join(folder, "%d.%s" % (self._id, self._type)))
#             except:
#                 try:
#                     download(self._thumbnail, os.path.join(folder, "%d_thrmbnail.%s" % (self._id, self._type)))
#                 except:
#                     with open(os.path.join(folder, "%d_placeholder.txt" % self._id)) as fp:
#                         fp.write("can not download")
#
#
#
#
#
#
#
# #
# class ClassCircle(object):
#     _id = -1
#     _pictures = []
#     _text = ""
#     _time = ""
#     _name = ""
#
#     def __init__(self, jo):
#         self._id = jo['id']
#         self._text = jo['content']
#         self._time = jo['createTime'].replace(' ', '_').replace(':', '-')
#
#         self._name = "%d_%s" % (self._id, self._time)
#
#         for picture in jo['ossResources']:
#             self._pictures.append(ClassCirclePicture(picture, self._id))
#
#
#     def download(self, folder):
#         datadir = os.path.join(folder, self._name)
#         if os.access(datadir, os.F_OK):
#             return False;
#         else:
#             tempdir = os.path.join(folder, self._id)
#             if os.access(tempdir, os.F_OK):
#                 os.rmdir(tempdir)
#
#             os.mkdir(tempdir)
#
#             with open(os.path.join(tempdir, 'content.txt'), 'w') as fp:
#                 fp.write(self._text)
#
#             for picture in self._pictures:
#                 picture.download(tempdir)
#
#             os.rename(tempdir, datadir)
#
#





# def build_from_json(jo):
#     ret = []
#     for jcc in jo['items']:
#         ret.append(ClassCircle(jcc))
#
#     return ret


def process_picture(folder, ccid, jo):
    id = jo['id']
    fnp = jo['fileName'].split('.')
    type = fnp[len(fnp) - 1]

    print("\tdownload picture %d-%d ..." % (ccid, id), end='')

    if True:
        try:
            jo1 = get('%s/class_circle_messages/%d/oss_resources/%d/origin_resource?platform=app' % (APP_SERVER, ccid, id))

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
        return False;
    else:
        tempdir = os.path.join(folder, str(id))
        if os.access(tempdir, os.F_OK):
            shutil.rmtree(tempdir)
            #os.rmdir(tempdir)

        os.mkdir(tempdir)

        with open(os.path.join(tempdir, 'content.txt'), 'w', encoding='utf8') as fp:
            text = jo['content']
            fp.write(text)


        for picture in jo['ossResources']:
            process_picture(tempdir, id, picture)

        os.rename(tempdir, datadir)

        print('class circle [%d] done' % id)





if __name__ == '__main__':
    items = []
#    login('13761240204', '123')
#    r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
#    items = r['item']
    with open('D:/work/ailejiao_clone/test/banjiquan.json', 'r', encoding='utf8') as fp:
        j = json.load(fp)
        for item in j['data']['items']:
            process_class_circle("d:/work/ailejiao_clone/test/", item)







