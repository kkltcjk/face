import os
import subprocess


def do_cluster(base_dir):
    input_dir = os.path.join(base_dir, 'output')
    second_cluster_dir = os.path.join(base_dir, 'cluster')

    _do_cluster(base_dir, input_dir, second_cluster_dir)


def _do_cluster(base_dir, input_dir, second_cluster_dir):
    with open(os.path.join(base_dir, 'result.log'), 'a+') as f:
        cmd = './mergeClusterSecond {} {}'.format(input_dir, second_cluster_dir))
        p = subprocess.Popen(cmd, shell=True, stdout=f.fileno(),
                             stderr=f.fileno(), executable='/bin/bash',
                             cwd='/root/temp_face/yitu_sdk_sj_crack20180308')
        p.communicate()


if __name__ == '__main__':
    pass
