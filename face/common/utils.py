import os
import logging
import subprocess
import zipfile
from datetime import datetime

from stevedore import extension

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def get_subclass(namespace, cclass, name):
    extension.ExtensionManager(namespace=namespace, invoke_on_load=False)
    try:
        return next((c for c in cclass.__subclasses__() if c.__name__ == name))
    except StopIteration:
        LOG.error('Cannot find subclass: %s', name)
        raise


def makedirs(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        LOG.warning('%s already exists', dirname)


def str_to_time(string, fformat):
    try:
        return datetime.strptime(string, fformat)
    except Exception:
        LOG.error('%s not match %s', string, fformat)


def format_timestamp(timestamp, fformat):
    return timestamp.strftime(fformat)


def exec_command(cmd, log_path, **kwargs):
    with open(log_path, 'a+') as f:
        p = subprocess.Popen(cmd,
                             shell=True,
                             stdout=f.fileno(),
                             stderr=f.fileno(),
                             executable='/bin/bash',
                             **kwargs)
    p.communicate()


def do_zip(output_file, base_dir):
    f = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_STORED)

    for dirpath, dirnames, filenames in os.walk(base_dir):

        first_basename = os.path.basename(dirpath)
        second_basename = os.path.basename(os.path.dirname(dirpath))
        sub_dir = os.path.join(second_basename, first_basename)

        for filename in filenames:
            f.write(base_dir, os.path.join(sub_dir, filename))

    f.close()
