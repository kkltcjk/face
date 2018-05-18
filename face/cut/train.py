from face.cut import Cut
from face.cut import Ipc


class TrainCutV1(Cut):
    def _get_ipc_object(self, ddir):
        return TrainIpcV1(self.conf, ddir)


class TrainIpcV1(Ipc):
    def _get_cmd(self):
        script = './{}'.format(self.conf.get('cut_cmd'))
        cmd_list = [script, self.ddir, self.video_dir, self.yitu_dir, self.output_dir]
        return ' '.join(cmd_list)
