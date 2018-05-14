# coding=utf-8

import os
import errno
import shutil


def handle_video(origin_dir, target_dir):
    if not os.path.exists(target_dir):
        makedirs(target_dir)

    new_dir = os.path.basename(origin_dir)
    copy_dir(origin_dir, os.path.join(target_dir, new_dir))
    move_video(new_dir)


def copy_dir(origin_dir, target_dir):
    shutil.copytree(origin_dir, target_dir)


def move_video(base_dir):
    for f in os.listdir(base_dir):
        move_to_video_dir(os.path.join(base_dir, f))


def move_to_video_dir(base_dir):
    for sub_dir in os.listdir(base_dir):
        sub_dir  = os.path.join(base_dir, sub_dir)
        video_dir = os.path.join(sub_dir, 'video')
        makedirs(video_dir)
        for f in os.listdir(sub_dir):
            if f.endswith('mp4'):
                shutil.move(os.path.join(sub_dir, f), os.path.join(video_dir, f))


def fullpath(dirname, name):
    return os.path.join(dirname, name)


def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    handle_video('/mnttrace/20180511', '/home')
