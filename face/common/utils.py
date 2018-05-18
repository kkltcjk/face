import os
import logging
import subprocess
from datetime import datetime

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


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
