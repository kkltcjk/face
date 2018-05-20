import os
import logging
import abc
import six

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Cluster(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.cluster_dir = os.path.join(ddir, 'cluster')
        self.image_dir = os.path.join(self.cluster_dir, 'output')
        self.log_path = os.path.join(self.cluster_dir, 'result.log')

        self.api_dir = self.conf.get('api_dir')

        if not os.path.exists(self.image_dir):
            raise RuntimeError('{} is not exists'.format(self.image_dir))

        if not os.path.isdir(self.image_dir):
            raise RuntimeError('{} is not dir'.format(self.image_dir))

    def run(self):
        LOG.info('%s start cluster job', self.ddir)

        self._run()

        LOG.info('%s cluster job finished', self.ddir)

    @abc.abstractmethod
    def _run(self):
        pass
