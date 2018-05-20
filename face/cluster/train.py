# coding=utf-8
import logging

from face.cluster import Cluster
from face.cluster.cluster import do_cluster

LOG = logging.getLogger(__name__)


class TrainClusterV1(Cluster):
    def _run(self):
        do_cluster(self.cluster_path, self.api_dir, self.log_path)
