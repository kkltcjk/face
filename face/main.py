import yaml
import io

from face.process.train import TrainProcessV1


def main(ddir):
    obj = TrainProcessV1(ddir)
    obj.run()


if __name__ == '__main__':
    ddir = '/mntticket/test'
    main([ddir])
