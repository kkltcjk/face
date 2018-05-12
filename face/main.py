from os.path import join
from os.path import basename

from prepare import handle_video
from cut import cut
from cluster import do_cluster


def main(origin_dir, target_dir):
    dir_name = basename(origin_dir)
    handle_video(origin_dir, target_dir)
    cut(join(target_dir, dir_name, 'IPC1'), join(target_dir, dir_name, 'IPC15'))
    do_cluster()


if __name__ == '__main__':
    origin_dir = ''
    target_dir = ''
    main(origin_dir, target_dir)
