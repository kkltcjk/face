# coding=utf-8
import os
import re
import logging

from face.prepare import Prepare
from face.common import utils

LOG = logging.getLogger(__name__)


class TrainPrepareV1(Prepare):
    def _adapt(self):
        self._create_ipc_dirs()
        self._move_mp4_to_ipc_dir()

    def _create_ipc_dirs(self):
        ipcs = self.conf.get('ipc_map', {})
        for ipc in ipcs:
            utils.makedirs(os.path.join(self.ddir, ipc))

    def _move_mp4_to_ipc_dir(self):
        for f in os.listdir(self.ddir):
            abs_path = os.path.join(self.ddir, f)
            if os.path.isfile(abs_path):
                if abs_path.endswith('mp4'):
                    self._move_mp4(abs_path)
                else:
                    os.remove(abs_path)

    def _move_mp4(self, path):
        file_name = os.path.basename(path)

        ipc = self._get_ipc(file_name)
        new_name = self._get_new_name(ipc, file_name)
        new_path = os.path.join(self.ddir, ipc, new_name)

        utils.move_file(path, new_path)

    def _get_ipc(self, file_name):
        rmap = self.conf.get('rmap', {})

        if re.search(r'(.*)验票口南球机(.*)', file_name):
            ipc = 'IPC1'
        elif re.search(r'(.*)安检大厅球机(.*)', file_name):
            ipc = 'IPC15'
        else:
            ipc = rmap[file_name.split('_')[1].upper()]

        return ipc

    def _get_new_name(self, ipc, file_name):
        timestamp = utils.str_to_time(file_name.split('_')[3], '%Y%m%d%H%M%S')

        time_str = utils.format_timestamp(timestamp, '%Y_%m_%d_%H_%M_%S')

        return '{}_{}.mp4'.format(ipc, time_str)
