# coding=utf-8
import os
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
    def __init__(self, process, conf, dirs):
        self.process = process

        self.classes = conf['classes'][process]
        self.conf = conf[process]

        self.dirs = dirs

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
                LOG.info('%s job finished', ddir)

    def _prepare(self, ddir):
        obj = self._class('prepare', Prepare, self.classes['prepare'])(self.conf, ddir)
        obj.run()

    def _cut(self, ddir):
        obj = self._class('cut', Cut, self.classes['cut'])(self.conf, ddir)
        obj.run()

    def _cluster(self, ddir):
        obj = self._class('cluster', Cluster, self.classes['cluster'])(self.conf, ddir)
        obj.run()

    def _class(self, namespace, base_class, class_name):
        return utils.get_subclass(namespace, base_class, class_name)

    def _between_job(self, ddir):
        pass

    def _do_zip(self, ddir):
        base_name = os.path.basename(ddir)
        output_dir = os.path.join(self.conf['output_dir'], base_name)
        result_dir = os.path.join(output_dir, 'cluster', 'result')
        zip_path = os.path.join(output_dir, '{}.zip'.format(base_name))
        utils.do_zip(zip_path, result_dir)
