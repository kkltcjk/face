# coding=utf-8
import os
import six
import abc
import logging
from multiprocessing import Pool

from face.prepare import Prepare
from face.cut import Cut
from face.cluster import Cluster
from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class Process(object):
    def __init__(self, process, conf, dirs):
        self.process = process

        self.classes = conf['classes'][process]
        self.conf = conf[process]

        self.dirs = dirs

        self.cluster_pool = Pool(4)
        self.cluster_class_name = self._get_cluster_class()

    def run(self):
        try:
            LOG.info('job started')

            self._prepare()
            self._cut()

            self._cluster()

        except Exception:
            LOG.exception('job failed')
        else:
            LOG.info('job finished')

    def _prepare(self):
        obj = self._class('prepare', Prepare, self.classes['prepare'])(self.conf, self.dirs)
        obj.run()

    def _cut(self):
        obj = self._class('cut', Cut, self.classes['cut'])(self.conf, self.dirs)
        obj.set_cluster_pool(self.cluster_pool)
        obj.set_cluster_class(self.cluster_class_name)
        obj.run()

    def _cluster(self):
        self.cluster_pool.close()
        self.cluster_pool.join()

    def _get_cluster_class(self):
        return self._class('cluster', Cluster, self.classes['cluster'])

    def _class(self, namespace, base_class, class_name):
        return utils.get_subclass(namespace, base_class, class_name)
