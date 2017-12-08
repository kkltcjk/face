import os
import subprocess


def cut(base_dir, output_dir):
    for sub in os.listdir(base_dir):
        if sub != 'cluster':
            sub_dir = os.path.join(base_dir, sub)
            video_dir = os.path.join(sub_dir, 'video')
            yitu_dir = os.path.join(sub_dir, 'yitu_orgin')
            _cut(sub_dir, video_dir, yitu_dir, output_dir)


def _cut(base_dir, video_dir, yitu_dir, output_dir):
    ipc_no = int(os.path.basename(base_dir).split('_')[1][3:]) * 100
    with open(os.path.join(base_dir, 'result.log'), 'a+') as f:
        cmd = './exe.sh {} {} {} {} {}'.format(base_dir, video_dir,
                                           yitu_dir, output_dir, ipc_no)
        p = subprocess.Popen(cmd, shell=True, stdout=f.fileno(),
                             stderr=f.fileno(), executable='/bin/bash',
                             cwd='/root/temp_face/yitu_sdk_sj_crack20180308')
        p.communicate()


if __name__ == '__main__':
    cut('/home/data/test/s8_20180503', '/home/data/test/s8_20180503/cluster/output')
