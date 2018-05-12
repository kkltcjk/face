from multiprocessing import Process

import utils


def cut(paths):
    process_list = [Process(target=_cut, args=(path,)) for path in paths]
    [p.start() for p in process_list]
    [p.join() for p in process_list]


def _cut(path):
    cmd = './run_z00355208_trace {}'.format(path)
    kwargs = {'cwd': '/root/temp_face/yitu_sdk_sj_crack20180308'}
    utils.execute_command(cmd, **kwargs)


if __name__ == '__main__':
    cut(['/home/data/20180511/IPC1', '/home/data/20180511/IPC15'])
