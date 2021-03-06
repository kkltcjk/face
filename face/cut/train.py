# coding=utf-8
import os
import logging

from face.cut import Cut
from face.cut import Ipc

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class TrainCutV1(Cut):
    def _get_ipc_object(self, ddir):
        return TrainIpcV1(self.conf, ddir)


class TrainIpcV1(Ipc):
    def _get_cmd(self):
        script = './{}'.format(self.conf['cut']['cmd'])
        width = self.conf['cut']['width']
        height = self.conf['cut']['height']

        self.config_file = 'config/config_{}.json'.format(self.gpu_no + 1)

        cmd_list = [
            script, self.ddir, self.video_dir, self.yitu_dir, self.output_dir,
            str(self.gpu_no + 1), self.config_file, str(width), str(height)
        ]

        return ' '.join(cmd_list)
