import os
import abc
import six
import multiprocessing

from face.common import utils


@six.add_metaclass(abc.ABCMeta)
class Cut(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.process_num = int(conf.get('process_num', 2))

    def run(self):
        pool = multiprocessing.Pool(self.process_num)

        for d in os.listdir(self.ddir):
            if d != 'cluster':
                ipc_dir = os.path.join(self.ddir, d)
                obj = self._get_ipc_object(ipc_dir)
                pool.apply_async(obj.run)

        pool.close()
        pool.join()

    @abc.abstractclass
    def _get_ipc_object(self, path):
        pass


@six.add_metaclass(abc.ABCMeta)
class Ipc(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.video_dir = os.path.join(ddir, 'video')
        self.yitu_dir = os.path.join(ddir, 'yitu_dir')
        self.log_path = os.path.join(ddir, 'result.log')

        scenario_dir = os.path.dirname(self.ddir)
        self.output_dir = os.path.join(scenario_dir, 'cluster', 'output')

    def run(self):
        cmd = self._get_cmd()
        self._run_cmd(cmd)

    @abc.abcstractmethod
    def _get_cmd(self):
        pass

    def _run_cmd(self, cmd):
        kwargs = {'cwd': self.conf.get('api_dir')}
        utils.exec_command(cmd, self.log_path, **kwargs)
