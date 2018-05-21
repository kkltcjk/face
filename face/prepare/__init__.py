# coding=utf-8
import os
import abc
import six
import logging

from face.common import utils

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Prepare(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

    def run(self):
        base_name = os.path.basename(self.ddir)
        LOG.info('%s start prepare job', base_name)

        self._adapt()

        self._create_video_dirs()

        self._move_mp4_to_video_dir()

        LOG.info('%s prepare job finished', base_name)

    @abc.abstractmethod
    def _adapt(self):
        pass

    def _create_video_dirs(self):
        for ddir in os.listdir(self.ddir):
            if ddir == 'cluster':
                continue
            abs_dir = os.path.join(self.ddir, ddir)
            if os.path.isdir(abs_dir):
                self._create_video_dir(abs_dir)

    def _create_video_dir(self, ddir):
        utils.makedirs(os.path.join(ddir, 'video'))

    def _move_mp4_to_video_dir(self):
        for ddir in os.listdir(self.ddir):
            if ddir == 'cluster':
                continue

            abs_dir = os.path.join(self.ddir, ddir)
            if not os.path.isdir(abs_dir):
                continue

            for f in os.listdir(abs_dir):
                abs_path = os.path.join(abs_dir, f)
                if os.path.isfile(abs_path):
                    self._move_file(abs_path)

    def _move_file(self, path):
        ddir = os.path.dirname(path)

        if path.endswith('mp4'):
            utils.move_file(path, os.path.join(ddir, 'video'))
        else:
            os.remove(path)
