import os

from face.cluster import Cluster
from face.cluster.cluster import do_cluster


class TrainClusterV1(Cluster):
    def run(self):
        cluster_path = os.path.join(self.ddir, 'cluster')
        do_cluster(cluster_path)
