import json
import io
import os
import os.path
from src.myhttp import login, get, APP_SERVER


class ClassCirclePicture(object):
    _id = -1
    _cc = -1
    _thumbnail = ''
    _normal = ''
    _original = ''

    def __init__(self, jo, ccid):
        self._cc = ccid
        self._id = jo['id']
        self._thumbnail = jo['thumbnailUrl']
        self._normal = jo['url']




#
class ClassCircle(object):
    _id = -1
    _pictures = []
    _text = ""
    _time = ""
    _name = ""

    def __init__(self, jo):
        self._id = jo['id']
        self._text = jo['content']
        self._time = jo['createTime'].replace(' ', '_').replace(':', '-')

        self._name = "%d_%s" % (self._id, self._time)

        for picture in jo['ossResources']:
            self._pictures.append(ClassCirclePicture(picture, self._id))


    def download(self, folder):
        t = os.access(os.path.join(folder, self._name))




def build_from_json(jo):
    ret = []
    for jcc in jo['items']:
        ret.append(ClassCircle(jcc))

    return ret









if __name__ == '__main__':
    items = []
#    login('13761240204', '123')
#    r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
#    items = r['item']
    with open('D:/work/ailejiao_clone/test/banjiquan.json', 'r', encoding='utf8') as fp:
        j = json.load(fp)
        for item in j['data']['items']:
            items.append(ClassCircle(item))


    for item in items:
        print(item)







