import os


class Cluster(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.cluster_dir = os.path.join(ddir, 'cluster')
        self.image_dir = os.path.join(self.cluster_dir, 'output')
        self.log_path = os.path.join(self.cluster_dir, 'result.log')
