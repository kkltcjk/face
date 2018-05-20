from face.common import utils
from face.common import constants as consts
from face.process import Process


def main(ddirs):
    conf = utils.parse_ymal(consts.CONFIG_FILE)
    class_name = conf['classes'][conf['process']]['process']
    obj = utils.get_subclass('process', Process, class_name)(conf, ddirs)
    obj.run()


if __name__ == '__main__':
    ddirs = ['/mntticket/test']
    main(ddirs)
