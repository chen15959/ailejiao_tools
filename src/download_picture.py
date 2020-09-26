from myhttp import prepare, get, APP_SERVER
from class_circle import process_class_circle
from config import Config
import json
import os
from datetime import datetime


print('login to server ... ', end='')
if prepare():
    print(' done')
    print('download class circle data ...', end='')
    r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
    print(' done')

    if Config().debug():
        with open(os.path.join(Config().get('download_folder'), '%s.json' % datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')), 'w') as fp:
            json.dump(r, fp)

    for item in r['items']:
        process_class_circle(Config().get('download_folder'), item)

    print('all done')
else:
    print(' failed')
