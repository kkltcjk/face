# coding=utf-8
import os
import logging

from face.cut import Cut
from face.cut import Ipc

LOG = logging.getLogger(__name__)


class MultiheadCutV1(Cut):
    def _get_ipc_object(self, ddir):
        return MultiheadIpcV1(self.conf, ddir)


class MultiheadIpcV1(Ipc):
    def _get_cmd(self):
        script = './{}'.format(self.conf.get('cut_cmd'))
        self.ipc_no = int(os.path.basename(self.ddir).split('_')[1][3:]) * 100

        cmd_list = [
            script, self.ddir, self.video_dir,
            self.yitu_dir, self.output_dir, self.ipc_no
        ]

        return ' '.join(cmd_list)
