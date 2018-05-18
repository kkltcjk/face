import os
from os import listdir
from os.path import join
from os.path import basename

from prepare import handle_video
from prepare import makedirs
from cut import cut
from cluster import do_cluster


def main(origin_dir, target_dir):
    dir_name = basename(origin_dir)
    # handle_video(origin_dir, target_dir)
    target_dir = os.path.join(target_dir, dir_name)

    output_dir = os.path.join(target_dir, 'cluster', 'output')
    if not os.path.exists(output_dir):
        makedirs(output_dir)

    cut([join(target_dir, d) for d in listdir(target_dir) if d != 'cluster'])

    do_cluster(os.path.join(target_dir, 'cluster'))


if __name__ == '__main__':
    origin_dir = '/mntresource/resource/train-test'
    target_dir = '/home/data'
    main(origin_dir, target_dir)
