# coding=utf-8

import os
import re
import errno
import shutil
from datetime import datetime

SCENARIO_MAP = {
    'IPC1': r'(.*)南(.*)',
    'IPC15': ''
}


def handle_video(origin_dir, target_dir):
    if not os.path.exists(target_dir):
        makedirs(target_dir)

    create_dirs(origin_dir)
    rebuild_dir(origin_dir)
    copy_dir(origin_dir, os.path.join(target_dir, os.path.basename(origin_dir)))


def create_dirs(path):
    for scenario in SCENARIO_MAP:
        makedirs(os.path.join(path, scenario, 'video'))

def rebuild_dir(path):
    for name in os.listdir(path):
        full_path = fullpath(path, name)
        if os.path.isfile(full_path):
            handler_file(full_path)
        else:
            pass


def copy_dir(origin_dir, target_dir):
    shutil.copytree(origin_dir, target_dir)


def handler_file(full_path):
    if os.path.basename(full_path).endswith('mp4'):
        handle_mp4(full_path)
    else:
        os.remove(full_path)


def handle_mp4(full_path):
    base_name = os.path.basename(full_path)
    dir_name = os.path.dirname(full_path)
    t = datetime.strptime(base_name.split()[1].split('_')[3], '%Y%m%d%H%M%S')

    if re.search(SCENARIO_MAP['IPC1'], base_name):
        scenario = 'IPC1'
    else:
        scenario = 'IPC15'

    new_name = '{}_{}.mp4'.format(scenario, t.strftime('%Y_%m_%d_%H_%M_%S'))

    new_path = os.path.join(dir_name, scenario, 'video', new_name)

    shutil.move(full_path, new_path)


def fullpath(dirname, name):
    return os.path.join(dirname, name)


def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    handle_video('/mnttrace/test', '/home/data')
