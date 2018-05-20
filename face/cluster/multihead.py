# coding=utf-8
import os
import logging

from face.cluster import Cluster
from face.common import utils

LOG = logging.getLogger(__name__)


class MultiheadClusterV1(Cluster):
    def _run(self):
        kwargs = {'cwd': self.api_dir}
        cmd = self._get_cmd()

        utils.exec_command(cmd, self.log_path, **kwargs)

    def _get_cmd(self):
        script = './{}'.format(self.conf.get('cluster_cmd'))
        second_cluster_dir = os.path.join(self.cluster_dir, 'cluster')

        cmd = [script, self.image_dir, second_cluster_dir]

        return ' '.join(cmd)
