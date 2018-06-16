# coding=utf-8
import os
import logging

from face.process import Process
from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class MultiheadProcessV1(Process):

    def _between_job(self, ddir):
        utils.makedirs(os.path.join(ddir, 'cluster', 'output'))
