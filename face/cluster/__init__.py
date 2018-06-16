import os
import logging
import abc
import six
import shutil

from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class Cluster(object):
    def __init__(self, conf, ddir):
        self.conf = conf

        self.scenario = os.path.basename(ddir)
        self.ddir = os.path.join(self.conf['output_dir'], self.scenario)

        self.cluster_dir = os.path.join(self.ddir, 'cluster')
        self.image_dir = os.path.join(self.cluster_dir, 'id_data_cut')
        self.log_path = os.path.join(self.cluster_dir, 'result.log')

        self.api_dir = self.conf.get('api_dir')
        self.identity_dir = self.get('identity_dir')
        self.zip_dir = self.conf.get('zip_dir')
        self.zip_pass = self.conf.get('zip_pass')

        if not os.path.exists(self.image_dir):
            raise RuntimeError('{} is not exists'.format(self.image_dir))

        if not os.path.isdir(self.image_dir):
            raise RuntimeError('{} is not dir'.format(self.image_dir))

    def run(self):

        LOG.info('%s start cluster job', self.ddir)
        try:
            self._run()
        except Exception:
            LOG.exception('Cluster: %s failed', self.ddir)
        else:
            LOG.info('%s cluster job finished', self.ddir)

            self._do_zip()
            self._remove_cut_dir()

    @abc.abstractmethod
    def _run(self):
        pass

    def _do_zip(self):
        base_name = os.path.basename(self.ddir)
        output_dir = os.path.join(self.conf['output_dir'], base_name)
        result_dir = os.path.join(output_dir, 'cluster', 'id_data_result')
        zip_path = os.path.join(self.zip_dir, '{}.zip'.format(base_name))

        LOG.debug('Start to zip: %s', self.ddir)
        try:
            utils.do_zip(zip_path, result_dir, self.zip_pass)
        except Exception:
            LOG.exception('Fail to zip: %s', self.ddir)
        else:
            LOG.debug('Zip file: %s successfully', self.ddir)

    def _remove_cut_dir(self):
        try:
            shutil.rmtree(self.ddir)
        except Exception:
            LOG.exception('Fail to remove cut dir: %s', self.ddir)
        else:
            LOG.debug('Remove cut dir: %s successfully', self.ddir)
