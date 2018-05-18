import os
import  multiprocessing

import utils


def cut(paths):
    pool = multiprocessing.Pool(processes = 3)
    for path in paths:
        pool.apply_async(_cut, (path, ))
    pool.close()
    pool.join()


def _cut(path):
    video_dir = os.path.join(path, 'video')
    yitu_dir = os.path.join(path, 'yitu_orgin')
    output_dir = os.path.join(os.path.dirname(path), 'cluster', 'output')
    cmd = './do_cut.sh {} {} {} {}'.format(path, video_dir, yitu_dir, output_dir)
    kwargs = {'cwd': '/home/kklt/train'}
    utils.execute_command(cmd, **kwargs)


if __name__ == '__main__':
    cut(['/home/data/test/IPC1', '/home/data/test/IPC15', '/home/data/test/IPC2'])
