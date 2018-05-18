import yaml
import io

from face.prepare.train import TrainPrepareV1
from face.cut.train import TrainCutV1


def main(ddir):
    conf = yaml.safe_load(io.open('/etc/face/face.conf', encoding='utf-8'))['train']

    obj = TrainCutV1(conf, '/mntticket/test')
    obj.run()


if __name__ == '__main__':
    ddir = '/mntticket/test'
    main([ddir])
