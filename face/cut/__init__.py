# coding=utf-8
import os
import abc
import six
import logging
import shutil
import subprocess

from face.common.pool import GPUPool
from face.cluster import Cluster
from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def _wapper(obj):
    obj.run()


@six.add_metaclass(abc.ABCMeta)
class Cut(object):
    def __init__(self, conf, ddirs):
        self.conf = conf
        self.ddirs = ddirs

        cut_conf = self.conf['cut']
        self.gpu_total = cut_conf['gpu']['total']
        self.gpu_process = cut_conf['gpu']['process']
        self.disk_total = cut_conf['disk']['total']
        self.blacklist =  cut_conf['blacklist']
        LOG.debug('GPU: %s, Process: %s, Disk: %s', self.gpu_total, self.gpu_process, self.disk_total)

        self.cluster_class = None

        self.cluster_pool = None

    def set_cluster_pool(self, cluster_pool):
        self.cluster_pool = cluster_pool

    def set_cluster_class(self, cluster_class):
        self.cluster_class = cluster_class

    def run(self):

        for ddir in self.ddirs:
            LOG.debug('Sync disk: %s', ddir)
            kwargs = {'cwd': ddir}
            utils.exec_command('du -h --max-depth=1', '/var/log/face/disk.log', **kwargs)


            ddir = os.path.join(self.ddirs, ddir)
            self._cut_single_day(ddir)


    def _cut_single_day(self, ddir):
        LOG.info('%s start cut job', ddir)

        count = 0

        pool = GPUPool(self.gpu_total, self.gpu_process)

        for d in os.listdir(ddir):
            if not d.startswith('IPC'):
                continue
            
            if d in self.blacklist:
                continue

            gpu_no = count % self.gpu_total
            disk_no = count % self.disk_total
            LOG.debug('%s will run on GPU: %s, Disk: %s', d, gpu_no, disk_no)

            ipc_dir = os.path.join(ddir, d)
            if os.path.isdir(ipc_dir):
                obj = self._get_ipc_object(ipc_dir)
                obj.update_gpu(gpu_no)
                obj.update_disk(disk_no)

                pool.apply_async(_wapper, (obj, ), gpu_no)

            count += 1


        pool.get()
        pool.close()
        pool.join()

        LOG.info('%s cut job finished', ddir)

        self._remove_cut_dir(ddir)
        try:
            self._remove_temp_dir(ddir)
        except Exception:
            LOG.exception('RM temp file failed')

        obj = self.cluster_class(self.conf, ddir)
        self.cluster_pool.apply_async(_wapper, (obj, ))

    def _remove_temp_dir(self, ddir):
        scenario = os.path.basename(ddir)
        for disk_no in range(self.disk_total):
            scenario_temp = os.path.join(self.conf['cut']['disk']['path'][disk_no], scenario)
            if os.path.exists(scenario_temp):
                shutil.rmtree(scenario_temp)

    @abc.abstractmethod
    def _get_ipc_object(self, path):
        pass

    def _remove_cut_dir(self, ddir):
        try:
            shutil.rmtree(ddir)
        except Exception:
            LOG.exception('Fail to remove cut dir: %s', ddir)
        else:
            LOG.debug('Remove cut dir: %s successfully', ddir)


@six.add_metaclass(abc.ABCMeta)
class Ipc(object):
    def __init__(self, conf, ddir):
        self.conf = conf
        self.ddir = ddir

        # self.video_dir = ''
        self.video_dir = os.path.join(self.ddir, 'video')

        self.ipc_no = 0
        self.gpu_no = 0
        self.disk_no = 0

        self.config_file = ''
        self.yitu_dir = ''
        self.log_path = ''
        self.output_dir = ''

    def _setup(self):
        disk_dir = self.conf['cut']['disk']['path'][self.disk_no]

        ipc_name = os.path.basename(self.ddir)
        scenario_name = os.path.basename(os.path.dirname(self.ddir))

        scenario_dir = os.path.join(disk_dir, scenario_name)
        target_dir = os.path.join(scenario_dir, ipc_name)

        # if not os.path.exists(scenario_dir):
        #     utils.makedirs(scenario_dir)

        # if os.path.exists(target_dir):
        #     shutil.rmtree(target_dir)
        # LOG.debug('Copy %s from %s to %s', ipc_name, self.ddir, target_dir)
        # shutil.copytree(self.ddir, target_dir)

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        utils.makedirs(target_dir)

        self.ddir = target_dir

        self.yitu_dir = os.path.join(self.ddir, 'yitu_dir')
        self.log_path = os.path.join(self.ddir, 'result.log')

        scenario_dir = os.path.join(self.conf['output_dir'], scenario_name)
        if not os.path.exists(scenario_dir):
            utils.makedirs(scenario_dir)

        self.output_dir = os.path.join(scenario_dir, 'cluster', 'id_data_cut')

        if not os.path.exists(self.video_dir):
            raise RuntimeError('{} is not exists'.format(self.video_dir))

        if not os.path.isdir(self.video_dir):
            raise RuntimeError('{} is not dir'.format(self.video_dir))

    def run(self):
        self._setup()

        LOG.debug('%s start sub cut job', self.ddir)

        cmd = self._get_cmd()
        self._run_cmd(cmd)

        self._remove_temp_dir()

        LOG.debug('%s sub cut job finished', self.ddir)

    def update_gpu(self, gpu_no):
        self.gpu_no = gpu_no

    def update_disk(self, disk_no):
        self.disk_no = disk_no

    @abc.abstractmethod
    def _get_cmd(self):
        pass

    def _run_cmd(self, cmd):
        kwargs = {'cwd': self.conf.get('api_dir')}
        utils.exec_command(cmd, self.log_path, **kwargs)

    def _remove_temp_dir(self):
        LOG.debug('Remove temp dir: %s', self.ddir)
        try:
            shutil.rmtree(self.ddir)
        except Exception:
            LOG.exception('Fail to remove temp dir: %s', self.ddir)
