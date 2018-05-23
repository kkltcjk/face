import logging
from multiprocessing import Pool
from multiprocessing import Lock

LOG = logging.getLogger(__name__)


class GPUPool(object):
    def __init__(self, conf, ttype):
        self.gpu = conf[ttype]['gpu']
        self.process = conf[ttype]['process']

        self.pools = {i: Pool(self.process) for i in range(self.gpu)}
        self.lock = Lock()

        self.count = 0

        self.task = []

    def apply_async(self, target, args):
        with self.lock:
            gpu_no = self.count % self.gpu
            self._update_gpu_no(args, gpu_no)

            self.task.append(self.pools[gpu_no].apply_async(target, args))

            self.count += 1

    def _update_gpu_no(self, args, gpu_no):
        try:
            args[0].update_gpu(gpu_no)
        except AttributeError:
            pass

    def close(self):
        [p.close() for p in self.pools.values()]

    def join(self):
        [p.join() for p in self.pools.values()]
