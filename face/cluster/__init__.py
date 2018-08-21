import os
import logging
import abc
import six
import shutil
import json
from collections import defaultdict

import requests
from face.common import utils

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@six.add_metaclass(abc.ABCMeta)
class Cluster(object):
    def __init__(self, conf, ddir):
        self.conf = conf

        self.scenario = os.path.basename(ddir)

        output_num = self.conf['output']['total']
        output_dir = self.conf['output']['path'][int(self.scenario) % output_num]

        self.ddir = os.path.join(output_dir, self.scenario)

        self.cluster_dir = os.path.join(self.ddir, 'cluster')
        self.image_dir = os.path.join(self.cluster_dir, 'id_data_cut')
        self.result_dir = os.path.join(self.cluster_dir, 'id_data_result')
        self.log_path = os.path.join(self.cluster_dir, 'result.log')

        self.api_dir = self.conf.get('api_dir')
        self.identity_dir = self.conf.get('identity_dir')
        self.zip_dir = self.conf.get('zip_dir')
        self.zip_pass = self.conf.get('zip_pass')

        if not os.path.exists(self.image_dir):
            raise RuntimeError('{} is not exists'.format(self.image_dir))

        if not os.path.isdir(self.image_dir):
            raise RuntimeError('{} is not dir'.format(self.image_dir))

    def run(self):

        LOG.info('%s start cluster job', self.ddir)
        try:
            self._run()
        except Exception:
            LOG.exception('Cluster: %s failed', self.ddir)
        else:
            LOG.info('%s cluster job finished', self.ddir)

            LOG.debug('upload identity information')
            self._upload_identity_data()

            # try:
            #     # self._do_zip()
            #     self._copy_to_clean_dir()
            # except Exception:
            #     LOG.exception('Fail to copy: %s', self.result_dir)
            # else:
            #     LOG.debug('Copy file: %s successfully', self.result_dir)
            #     self._remove_cut_dir()

    @abc.abstractmethod
    def _run(self):
        pass

    def _upload_identity_data(self):
        result_dir = os.path.join(self.cluster_dir, 'id_data_result')
        for ddir in os.listdir(self.result_dir):
            abs_path = os.path.join(self.result_dir, ddir)
            identity_data = IdentityData(abs_path, self.conf)
            identity_data.run()

    def _copy_to_clean_dir(self):
        target_dir = os.path.join(self.conf['clean_dir'], self.scenario)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(self.result_dir, target_dir)

    def _do_zip(self):
        result_dir = os.path.join(self.ddir, 'cluster', 'id_data_result')
        zip_path = os.path.join(self.zip_dir, self.scenario)

        LOG.debug('Start to zip: %s', self.ddir)
        utils.do_zip(zip_path, result_dir, self.zip_pass)

    def _remove_cut_dir(self):
        try:
            shutil.rmtree(self.ddir)
        except Exception:
            LOG.exception('Fail to remove cut dir: %s', self.ddir)
        else:
            LOG.debug('Remove cut dir: %s successfully', self.ddir)


class IdentityData(object):
    def __init__(self, ddir, conf):
        self.ddir = ddir
        self.conf = conf

        self.faceid = os.path.basename(ddir)
        self.no = self.id_num_decoder(self.faceid)

        self.no_dir = os.path.join(self.conf['photo_dir'], self.no)

    def run(self):
        info = self._get_identity_info()

        if not os.path.exists(self.no_dir):
            os.makedirs(self.no_dir)

        identity_pic = self._copy_identity_img()
        faces = self._copy_face_img()

        data = {
            'no': self.no,
            'photo': identity_pic,
            'faces': faces
        }
        data.update(info)

        self._send_data(data)

    def _get_identity_info(self):
        with open(os.path.join(self.ddir, '{}.json'.format(self.faceid))) as f:
            info = json.load(f)
        return info

    def _copy_identity_img(self):
        identity_pic = os.path.join(self.no_dir, '{}.jpg'.format(self.faceid))
        if not os.path.exists(identity_pic):
            shutil.copyfile(os.path.join(self.ddir, '{}.jpg'.format(self.faceid)), identity_pic)

        return identity_pic

    def _copy_face_img(self):
        faces = defaultdict(list)

        for f in os.listdir(self.ddir):
            if not f.startswith(self.faceid):
                ipc = f.split('_')[0]
                faces[ipc].append(os.path.join(self.ddir, f))

        for ipc in faces:
            faces[ipc].sort()

            ipc_dir = os.path.join(self.no_dir, ipc)
            if not os.path.exists(ipc_dir):
                os.makedirs(ipc_dir)
            filename = os.path.basename(faces[ipc][0])
            targetfile = os.path.join(ipc_dir, filename)
            if not os.path.exists(targetfile):
                shutil.copyfile(faces[ipc][0], targetfile)

            faces[ipc] = targetfile

        return faces

    def _send_data(self, data):
        headers = {'Content-Type': 'application/json'}
        # url = 'http://{}/information/upload'.format(self.conf['photo_server'])
        url = 'http://{}/information/upload'.format('43.33.26.40:1111')
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        print resp.text

    def id_num_decoder(self, iid):
        key_first = ["A","B","C","D","E","F","G","H","I","J","K"]
        key = ["Q", "W", "E", "A", "S", "D", "T", "Y", "U", "R", "I", "O", "P", "F", "G", "H", "J"]

        first_num = key_first.index(iid[0])
        new_id = ""
        new_key = key[first_num+1:] + key[0:first_num+1]
        for i in range(0,len(iid)):
            if i == 0:
                new_id = new_id + str(first_num)
            else:
                if new_key.index(iid[i]) != 10:
                    new_id = new_id + str(new_key.index(iid[i]))
                else:
                    new_id = new_id + "X"

        return new_id


if __name__ == '__main__':
    result_dir = '/disk5/cut/20180730/cluster/id_data_result/EUTYYYTGGFDTYPYIYO'
    import yaml
    with open('/etc/face/face.conf') as f:
        conf = yaml.safe_load(f)['train']
    data = IdentityData(result_dir, conf)
    data.run()
    # for ddir in os.listdir(result_dir):
    #     abs_path = os.path.join(result_dir, ddir)
    #     data = IdentityData(abs_path, conf)
    #     data.run()
