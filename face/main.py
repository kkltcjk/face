from face.common import utils
from face.common import constants as consts
from face.process import Process


def main(process, ddirs):
    conf = utils.parse_ymal(consts.CONFIG_FILE)
    cclass = conf['classes'][process]['process']
    obj = utils.get_subclass('process', Process, cclass)(process, conf, ddirs)
    obj.run()


if __name__ == '__main__':
    process = 'train'
    ddirs = ['/43.33.26.79/d/20180721']

    main(process, ddirs)
