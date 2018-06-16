# coding=utf-8
import os
import abc
import six
import logging

from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class Prepare(object):
    def __init__(self, conf, ddirs):
        self.conf = conf
        self.ddirs = ddirs

    def run(self):
        for ddir in self.ddirs:
            base_name = os.path.basename(ddir)
            LOG.info('%s start prepare job', base_name)

            self._adapt(ddir)

            self._create_video_dirs(ddir)

            self._move_mp4_to_video_dir(ddir)

            LOG.info('%s prepare job finished', base_name)

    @abc.abstractmethod
    def _adapt(self, ddir):
        pass

    def _create_video_dirs(self, ddir):
        for dddir in os.listdir(ddir):
            if not dddir.startswith('IPC'):
                continue
            abs_dir = os.path.join(ddir, dddir)
            if os.path.isdir(abs_dir):
                self._create_video_dir(abs_dir)

    def _create_video_dir(self, ddir):
        video_dir = os.path.join(ddir, 'video')
        if not os.path.exists(video_dir):
            utils.makedirs(video_dir)

    def _move_mp4_to_video_dir(self, ddir):
        for dddir in os.listdir(ddir):
            if not dddir.startswith('IPC'):
                continue

            abs_dir = os.path.join(ddir, dddir)
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
            try:
                os.remove(path)
            except Exception:
                LOG.exception('Fail to remove %s', path)
