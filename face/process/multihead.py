# coding=utf-8
import os
import logging

from face.process import Process
from face.common import utils

LOG = logging.getLogger(__name__)


class MultiheadProcessV1(Process):

    def _between_job(self, ddir):
        for d in os.listdir(ddir):
            abs_dir = os.path.abspath(d)
            utils.makedirs(os.path.join(abs_dir, 'cluster', 'output'))
