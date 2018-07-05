import os
import logging
import subprocess
import zipfile
import shutil
from datetime import datetime

import yaml
from stevedore import extension
from retrying import retry

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def get_subclass(namespace, cclass, name):
    extension.ExtensionManager(namespace=namespace, invoke_on_load=False)
    try:
        return next((c for c in cclass.__subclasses__() if c.__name__ == name))
    except StopIteration:
        LOG.error('Cannot find subclass: %s', name)
        raise


def parse_ymal(path):
    if not os.path.exists(path):
        raise RuntimeError('file does not exist')

    with open(path) as f:
        conf = yaml.safe_load(f)

    return conf


@retry(stop_max_attempt_number=5, wait_fixed=1)
def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        LOG.warning('%s already exists', dirname)
    else:
        if not os.path.exists(dirname):
            raise Exception('Create dir {} failed'.format(dirname))


def move_file(origin, target):
    if not os.path.exists(origin):
        LOG.error('%s is not exists', origin)
        return
    if not os.path.isfile(origin):
        LOG.error('%s is not a file', origin)
        return

    dir_name = os.path.dirname(target)
    if not os.path.exists(dir_name):
        makedirs(dir_name)

    # LOG.debug('move file %s to %s', origin, target)
    try:
        shutil.move(origin, target)
    except Exception:
        LOG.exception('Fail to move %s to %s', origin, target)


def str_to_time(string, fformat):
    try:
        return datetime.strptime(string, fformat)
    except Exception:
        LOG.error('%s not match %s', string, fformat)


def format_timestamp(timestamp, fformat):
    return timestamp.strftime(fformat)


def exec_command(cmd, log_path, **kwargs):
    LOG.debug('execute command: %s', cmd)
    with open(log_path, 'w') as f:
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=f.fileno(),
                             stderr=f.fileno(),
                             executable='/bin/bash',
                             **kwargs)
    p.communicate()

    if p.returncode != 0:
        LOG.error('cmd: %s execute failed', cmd)
    else:
        LOG.debug('execute command: %s finished', cmd)

    return p.returncode


def do_zip(output_file, base_dir, zip_pass):
    LOG.debug('zip dir %s to %s', base_dir, output_file)

    cmd = 'zip -P {} -r {} *'.format(zip_pass, output_file)
    log_path = '/var/log/face/zip.log'
    kwargs = {'cwd': base_dir}
    returncode = exec_command(cmd, log_path, **kwargs)

    if returncode != 0:
        raise RuntimeError('zip {} failed'.format(base_dir))
    else:
        LOG.debug('zip dir %s finished', base_dir)
