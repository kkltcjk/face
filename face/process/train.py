import os

from face.process import Process
from face.prepare.train import TrainPrepareV1
from face.cut.train import TrainCutV1
from face.cluster.train import TrainClusterV1
from face.common import utils


class TrainProcessV1(Process):

    def __init__(self, dirs):
        super(TrainProcessV1, self).__init__(dirs)
        self.conf = self.conf['train']

    def _prepare(self):
        obj = TrainPrepareV1(self.conf, self.dirs)
        obj.run()

    def _cut(self, ddir):
        obj = TrainCutV1(self.conf, ddir)
        obj.run()

    def _between_job(self, ddir):
        for d in os.listdir(ddir):
            full_path = os.path.join(ddir, d)
            utils.makedirs(os.path.join(full_path, 'cluster', 'output'))

    def _cluster(self, ddir):
        obj = TrainClusterV1(self.conf, ddir)
        obj.run()
