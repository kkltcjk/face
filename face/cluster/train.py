# coding=utf-8
import os
import logging
import time
import shutil

from face.cluster import Cluster
from face.cluster.cluster import do_cluster

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class TrainClusterV1(Cluster):
    def _run(self):
        self._copy_identity_dir()
        self._copy_ticket_dir()

        do_cluster(self.cluster_dir, self.api_dir, self.log_path)

    def _copy_identity_dir(self):
        identity_dir = os.path.join(self.identity_dir, self.scenario, 'id_data_cluster') 
        if not os.path.exists(identity_dir):
            raise RuntimeError('identity dir does not exists')

        target_dir = os.path.join(self.cluster_dir, 'id_data_cluster')
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        LOG.debug('Copy identity dir')
        shutil.copytree(identity_dir, target_dir)

    def _copy_ticket_dir(self):
        ticket_dir = os.path.join(self.identity_dir, self.scenario, 'id_data_ticket') 
        if not os.path.exists(ticket_dir):
            raise RuntimeError('ticket dir does not exists')

        target_dir = os.path.join(self.cluster_dir, 'id_data_ticket')
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        LOG.debug('Copy ticket dir')
        shutil.copytree(ticket_dir, target_dir)
