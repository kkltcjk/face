import os
import six
import abc
import logging

import yaml

from face.common import constants as consts

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class Process(object):
    def __init__(self, dirs):
        self.dirs = dirs
        self.conf = self._read_config()

    def _read_config(self):
        if not os.path.exists(consts.CONFIG_FILE):
            raise RuntimeError('Config file does not exist')

        with open(consts.CONFIG_FILE) as f:
            conf = yaml.safe_load(f)

        return conf

    def run(self):
        for ddir in self.dirs:
            self._prepare(ddir)
            self._cut(ddir)
            self._between_job(ddir)
            self._cluster(ddir)
            self._do_zip(ddir)

    @abc.abstractmethod
    def _prepare(self, ddir):
        pass

    @abc.abstractmethod
    def _cut(self, ddir):
        pass

    def _between_job(self, ddir):
        pass

    @abc.abstractmethod
    def _cluster(self, ddir):
        pass

    def _do_zip(self, ddir):
        pass
