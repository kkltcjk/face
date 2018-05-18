import os
import six
import abc
import logging

import yaml

from face.common import constants import consts

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
        self._prepare()
        self._cut()
        self._between_job()
        self._cluster()
        self._do_zip()

    @abc.abstractmethod
    def _prepare(self):
        pass

    @abc.abstractmethod
    def _cut(self):
        pass

    @abc.abstractmethod
    def _between_job(self):
        pass

    @abc.abstractmethod
    def _cluster(self):
        pass

    def _do_zip(self):
        pass
