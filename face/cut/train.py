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
        self.ipc_no = int(os.path.basename(self.ddir)[3:]) * 100
        width = self.conf['cut']['width']
        height = self.conf['cut']['height']
        cmd_list = [
            script, self.ddir, self.video_dir, self.yitu_dir, self.output_dir,
            str(self.ipc_no), str(self.gpu_no), str(width), str(height)
        ]
        return ' '.join(cmd_list)

    def update_gpu(self, gpu_no):
        self.gpu_no = gpu_no
