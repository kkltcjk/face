import os
import re
import shutil

from face.prepare import Prepare
from face.common import utils


class TrainPrepareV1(Prepare):
    def __init__(self, conf, dirs):
        self.conf = conf
        self.dirs = dirs

    def run(self):
        for ddir in self.dirs:
            full_path = os.path.join(self.dirs, ddir)
            self._run_each_dir(full_path)

    def _run_each_dir(self, ddir):
        self._create_video_dirs(ddir)

    def _create_video_dirs(self, ddir):
        scenarios = self.conf.get('scenario_map', {})
        for scenario in scenarios:
            self._create_video_dir(ddir, scenario)

    def _create_video_dir(self, ddir, scenario):
        utils.makedirs(os.path.join(ddir, scenario, 'video'))

    def _rebuild_dir(self, ddir):
        for f in os.listdir(ddir):
            full_path = os.path.join(ddir, f)
            if os.path.isifle(full_path):
                self._handle_file(full_path)

    def _handle_file(self, path):
        if path.startswith('mp4'):
            self._handle_mp4(path)
        else:
            os.remove(path)

    def _handle_mp4(self, path):
        file_name = os.path.basename(path)
        dir_name = os.path.dirname(path)

        scenario = self._get_scenario(file_name)
        new_name = self._get_new_name(scenario, file_name)
        new_path = os.path.join(dir_name, scenario, 'video', new_name)

        shutil.move(path, new_path)

    def _get_scenario(self, file_name):
        scenarios = self.conf.get('scenario_map', {})
        rmap = self.conf.get('rmap', {})

        if re.search(scenarios['IPC1'], file_name):
            scenario = 'IPC1'
        elif re.search(scenarios['IPC15'], file_name):
            scenario = 'IPC15'
        else:
            scenario = rmap[file_name.split('_')[1].upper()]

        return scenario

    def _get_new_name(self, scenario, file_name):
        timestamp = utils.str_to_time(file_name.split('_')[3], '%Y%m%d%H%M%S')

        time_str = utils.format_timestamp(timestamp, '%Y_%m_%d_%H_%M_%S')

        return '{}_{}.mp4'.format(scenario, time_str)
