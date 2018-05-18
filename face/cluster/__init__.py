import os


class Cluster(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.image_dir = os.path.join(ddir, 'cluster', 'output')
