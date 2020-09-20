from myhttp import prepare, get, APP_SERVER
from class_circle import process_class_circle
from config import Config



if __name__ == '__main__':
    if prepare():
        print('download class circle data ...', end='')
        r = get(APP_SERVER + "/class_circle_messages/?currentPage=1&pageSize=1000&platform=app")
        print(' done')
        for item in r['items']:
            process_class_circle(Config().get('download_folder'), item)
