# coding=utf-8
import os
import abc
import six
import logging
import shutil
# from  multiprocessing import Pool
from face.common.pool import GPUPool

from face.common import utils

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Cut(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.process_num = int(conf.get('process_num', 2))

    def run(self):
        LOG.info('%s start cut job', self.ddir)

        # pool = Pool(processes=self.process_num)
        pool = GPUPool(self.conf, 'cut')

        for d in os.listdir(self.ddir):
            if d == 'cluster':
                continue
            if d in ['IPC22', 'IPC21', 'IPC1', 'IPC10', 'IPC20', 'IPC11', 'IPC16', 'IPC25', 'IPC18', 'IPC26', 'IPC23', 'IPC19', 'IPC34', 'IPC17', 'IPC24', 'IPC2', 'IPC29', 'IPC37', 'IPC35', 'IPC36', 'IPC28', 'IPC27']:
                LOG.debug('%s Pass', d)
                continue

            ipc_dir = os.path.join(self.ddir, d)
            if os.path.isdir(ipc_dir):
                obj = self._get_ipc_object(ipc_dir)
                pool.apply_async(_wapper, (obj, ))

        for p in pool.task:
            LOG.debug(p.get())

        pool.close()
        pool.join()

        LOG.info('%s cut job finished', self.ddir)

    @abc.abstractmethod
    def _get_ipc_object(self, path):
        pass


def _wapper(obj):
    obj.run()


@six.add_metaclass(abc.ABCMeta)
class Ipc(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        self.ipc_no = 0

        self.gpu_no = 0

        self.config_file = 'config/config_0.json'

    def _setup(self):
        disk_dir = self.conf['cut']['disk'][self.gpu_no]

        ipc_name = os.path.basename(self.ddir)
        scenario_name = os.path.basename(os.path.dirname(self.ddir))
        scenario_dir = os.path.join(disk_dir, scenario_name)
        target_dir = os.path.join(scenario_dir, ipc_name)
        if not os.path.exists(scenario_dir):
            utils.makedirs(scenario_dir)
        LOG.debug('Copy %s to %s', self.ddir, target_dir)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(self.ddir, target_dir)
        self.ddir = target_dir

        self.video_dir = os.path.join(self.ddir, 'video')
        self.yitu_dir = os.path.join(self.ddir, 'yitu_dir')
        self.log_path = os.path.join(self.ddir, 'result.log')

        scenario_dir = os.path.join(self.conf['output_dir'], scenario_name)
        if not os.path.exists(scenario_dir):
            utils.makedirs(scenario_dir)

        self.output_dir = os.path.join(scenario_dir, 'cluster', 'output')

        if not os.path.exists(self.video_dir):
            raise RuntimeError('{} is not exists'.format(self.video_dir))

        if not os.path.isdir(self.video_dir):
            raise RuntimeError('{} is not dir'.format(self.video_dir))

    def run(self):
        LOG.debug('Setup')
        self._setup()

        LOG.debug('%s start sub cut job', self.ddir)

        cmd = self._get_cmd()
        self._run_cmd(cmd)

        LOG.debug('%s sub cut job finished', self.ddir)

    def update_gpu(self, gpu_no):
        pass

    @abc.abstractmethod
    def _get_cmd(self):
        pass

    def _run_cmd(self, cmd):
        kwargs = {'cwd': self.conf.get('api_dir')}
        utils.exec_command(cmd, self.log_path, **kwargs)
