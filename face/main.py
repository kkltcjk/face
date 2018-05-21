from face.common import utils
from face.common import constants as consts
from face.process import Process


def main(process, ddirs):
    conf = utils.parse_ymal(consts.CONFIG_FILE)
    cclass = conf['classes'][process]['process']
    obj = utils.get_subclass('process', Process, cclass)(process, conf, ddirs)
    obj.run()


if __name__ == '__main__':
    process = 'multihead'
    ddirs = ['/mntresource/test/s2_20180427']

    main(process, ddirs)
