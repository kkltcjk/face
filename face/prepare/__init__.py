import os
import abc
import six
import shutil

from face.common import utils


@six.add_metaclass(abc.ABCMeta)
class Prepare(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

    def run(self):
        self._adapt()

        self._create_video_dirs()

        self._move_mp4_to_video_dir()

    @abc.abstractmethod
    def _adapt(self):
        pass

    def _create_video_dirs(self):
        for ddir in os.listdir(self.ddir):
            self._create_video_dir(os.path.abspath(ddir))

    def _create_video_dir(self, ddir):
        utils.makedirs(os.path.join(ddir, 'video'))

    def _move_mp4_to_video_dir(self):
        for ddir in os.listdir(self.ddir):
            full_path = os.path.abspath(ddir)
            for sub_dir in os.listdir(full_path):
                if os.path.isfile(full_path):
                    self._move_file(os.path.abspath(sub_dir))

    def _move_file(self, path):
        ddir = os.path.dirname(path)

        if path.endswith('mp4'):
            shutil.move(path, os.path.join(ddir, 'video'))
        else:
            os.remove(path)
