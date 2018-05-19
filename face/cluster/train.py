from face.cluster import Cluster
from face.cluster.cluster import do_cluster


class TrainClusterV1(Cluster):
    def run(self):
        do_cluster(self.cluster_path)
