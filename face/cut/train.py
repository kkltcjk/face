# coding=utf-8
import os
import logging

from face.cut import Cut
from face.cut import Ipc

LOG = logging.getLogger(__name__)


class TrainCutV1(Cut):
    def _get_ipc_object(self, ddir):
        return TrainIpcV1(self.conf, ddir)


class TrainIpcV1(Ipc):
    def _get_cmd(self):
        script = './{}'.format(self.conf['cut']['cmd'])
        self.config_file = 'config/config_{}.json'.format(self.gpu_no)
        width = self.conf['cut']['width']
        height = self.conf['cut']['height']
        cmd_list = [
            script, self.ddir, self.video_dir, self.yitu_dir, self.output_dir,
            str(self.gpu_no), self.config_file, str(width), str(height)
        ]
        return ' '.join(cmd_list)

    def update_gpu(self, gpu_no):
        self.gpu_no = gpu_no
