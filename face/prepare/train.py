# coding=utf-8
import os
import re
import logging

from face.prepare import Prepare
from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class TrainPrepareV1(Prepare):
    def _adapt(self, ddir):
        self._move_mp4_to_ipc_dir(ddir)

    def _move_mp4_to_ipc_dir(self, ddir):
        for f in os.listdir(ddir):
            abs_path = os.path.join(ddir, f)
            if os.path.isfile(abs_path):
                if abs_path.endswith('mp4'):
                    self._move_mp4(abs_path)
                else:
                    try:
                        os.remove(abs_path)
                    except Exception:
                        LOG.exception('Fail to remove %s', abs_dir)

    def _move_mp4(self, path):
        file_name = os.path.basename(path)
        ddir = os.path.dirname(path)

        ipc = file_name.split('_')[0]
        try:
            new_name = self._get_new_name(ipc, file_name)
        except AttributeError:
            return

        ipc_dir = os.path.join(ddir, ipc)
        if not os.path.exists(ipc_dir):
            utils.makedirs(ipc_dir)
        new_path = os.path.join(ipc_dir, new_name)

        utils.move_file(path, new_path)

    def _get_new_name(self, ipc, file_name):
        timestamp = utils.str_to_time(file_name.split('_')[3], '%Y-%m-%d-%H-%M-%S')

        time_str = utils.format_timestamp(timestamp, '%Y_%m_%d_%H_%M_%S')

        return '{}_{}.mp4'.format(ipc, time_str)
