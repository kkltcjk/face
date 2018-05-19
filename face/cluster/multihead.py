import os

from face.cluster import Cluster
from face.common import utils


class MultiheadClusterV1(Cluster):
    def run(self):
        kwargs = {'cwd': self.conf.get('api_dir')}
        cmd = self._get_cmd()

        utils.exec_command(cmd, self.log_path, **kwargs)

    def _get_cmd(self):
        script = './{}'.format(self.conf.get('cluster_cmd'))
        second_cluster_dir = os.path.join(self.cluster_dir, 'cluster')

        cmd = [script, self.image_dir, second_cluster_dir]

        return ' '.join(cmd)
