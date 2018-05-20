# coding=utf-8
import logging

from face.cluster import Cluster
from face.cluster.cluster import do_cluster

LOG = logging.getLogger(__name__)


class TrainClusterV1(Cluster):
    def run(self):
        do_cluster(self.cluster_path)
