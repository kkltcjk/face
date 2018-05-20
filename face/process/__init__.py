# coding=utf-8
import six
import abc
import logging

from face.prepare import Prepare
from face.cut import Cut
from face.cluster import Cluster
from face.common import utils

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Process(object):
    def __init__(self, conf, dirs):
        self.dirs = dirs

        self.process = conf['process']
        self.classes = conf['classes'][self.process]
        self.conf = conf[self.process]

    def run(self):
        for ddir in self.dirs:
            try:
                LOG.info('%s job started', ddir)

                self._prepare(ddir)
                self._cut(ddir)
                self._between_job(ddir)
                self._cluster(ddir)
                self._do_zip(ddir)
            except Exception:
                LOG.exception('%s job failed', ddir)
            else:
                LOG.indo('%s job finished', ddir)

    def _prepare(self, ddir):
        obj = self._class(Prepare, self.classes['prepare'])(self.conf, ddir)
        obj.run()

    def _cut(self, ddir):
        obj = self._class(Cut, self.classes['cut'])(self.conf, ddir)
        obj.run()

    def _cluster(self, ddir):
        obj = self._class(Cluster, self.classes['cluster'])(self.conf, ddir)
        obj.run()

    def _class(self, base_class, class_name):
        return utils.get_subclass(self.process, base_class, class_name)

    def _between_job(self, ddir):
        pass

    def _do_zip(self, ddir):
        pass
