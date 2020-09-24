from myhttp import prepare, get, APP_SERVER
from class_circle import praise_class_circle
from config import Config
import json
import os
from datetime import datetime



if prepare():
    print('download class circle data ...', end='')
    r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
    print(' done')

    if Config().debug():
        with open(os.path.join(Config().get('download_folder'), '%s.json' % datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')), 'w') as fp:
            json.dump(r, fp)

    for item in r['items']:
        praise_class_circle(item)

    print('all done')
