# coding=utf-8
import os
import abc
import six
import logging
import multiprocessing

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

        pool = multiprocessing.Pool(processes=self.process_num)

        for d in os.listdir(self.ddir):
            if d == 'cluster':
                continue

            ipc_dir = os.path.abspath(d)
            if os.path.isdir(ipc_dir):
                obj = self._get_ipc_object(ipc_dir)
                pool.apply_async(_wapper, (obj, ))

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

        self.video_dir = os.path.join(ddir, 'video')
        self.yitu_dir = os.path.join(ddir, 'yitu_dir')
        self.log_path = os.path.join(ddir, 'result.log')

        scenario_dir = os.path.dirname(self.ddir)
        self.output_dir = os.path.join(scenario_dir, 'cluster', 'output')

        self.ipc_no = 0

        if not os.path.exists(self.video_dir):
            raise RuntimeError('{} is not exists'.format(self.video_dir))

        if not os.path.isdir(self.video_dir):
            raise RuntimeError('{} is not dir'.format(self.video_dir))

    def run(self):
        LOG.debug('%s start sub cut job', self.ddir)

        cmd = self._get_cmd()
        self._run_cmd(cmd)

        LOG.debug('%s sub cut job finished', self.ddir)

    @abc.abstractmethod
    def _get_cmd(self):
        pass

    def _run_cmd(self, cmd):
        kwargs = {'cwd': self.conf.get('api_dir')}
        utils.exec_command(cmd, self.log_path, **kwargs)
