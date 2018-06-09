# from face.prepare.train import TrainPrepareV1
from face.cut.train import TrainCutV1
from face.common.utils import parse_ymal
from face.common import constants as consts


def main(ttype, ddirs):
    conf = parse_ymal(consts.CONFIG_FILE)[ttype]
    for ddir in ddirs:
        # obj = TrainPrepareV1(conf, ddir)
        obj = TrainCutV1(conf, ddir)
        obj.run()


if __name__ == '__main__':
    ttype = 'train'
    ddirs = ['/home/share1/20180601']
    main(ttype, ddirs)
