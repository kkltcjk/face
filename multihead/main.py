import os

from prepare import handle_video
from prepare import makedirs
from cut import cut
from cluster import do_cluster
from compress import do_zip


def main(target_dir):
    handle_video(target_dir)
    # target_dir = os.path.join(target_dir, os.path.basename(origin_dir))
    for f in os.listdir(target_dir):
        print('Task: {} start'.format(f))
        try:
            scenario_dir = os.path.join(target_dir, f)
            output_dir = os.path.join(scenario_dir, 'cluster', 'output')
            cut(scenario_dir, output_dir)
            cluster_dir = os.path.join(scenario_dir, 'cluster', 'cluster')
            makedirs(cluster_dir)
            do_cluster(os.path.join(scenario_dir, 'cluster'))
            zip_file = os.path.join(scenario_dir, '{}.zip'.format(os.path.basename(scenario_dir)))
            do_zip(zip_file, cluster_dir)
        except Exception as e:
            print('Task: {} error'.format(f))
            print(e)


if __name__ == '__main__':
    # origin_dir = '/mnttest/s8_20180429_20180503'
    target_dir = '/mnttest/s8_20180429_20180503'
    main(target_dir)
