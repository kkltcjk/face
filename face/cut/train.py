# coding=utf-8
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
        cmd_list = [
            script, self.ddir, self.video_dir,
            self.yitu_dir, self.output_dir, self.gpu_no
        ]
        return ' '.join(cmd_list)

    def update_gpu(self, gpu_no):
        self.gpu_no = gpu_no
