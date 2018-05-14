import os
import subprocess


def cut(base_dir, output_dir):
    for sub in os.listdir(base_dir):
        if sub != 'cluster':
            sub_dir = os.path.join(base, sub)
            video_dir = os.path.join(sub_dir, 'video')
            yitu_dir = os.path.join(sub_dir, 'yitu_orgin')


def _cut(base_dir, video_dir, yitu_dir, output_dir):
    ipc_no = os.path.basename(base_dir).split('_')[1][-1]
    with open(os.path.join(base_dir, 'result.log'), 'a+') as f:
        script = 'face_verify_video_sample_jiankong'
        cmd = './{} {} {} {} {} {}'.format(script, base_dir, video_dir,
                                           yitu_dir, output_dir, ipc_no)
        p = subprocess.Popen(cmd, shell=True, stdout=f.fileno(),
                             stderr=f.fileno(), executable='/bin/bash',
                             cwd='/root/temp_face/yitu_sdk_sj_crack20180308')
        p.communicate()


if __name__ == '__main__':
    cut(['/home/data/20180511/IPC1', '/home/data/20180511/IPC15'])
