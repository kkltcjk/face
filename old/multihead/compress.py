import os

import zipfile

def do_zip(output_file, base_dir):
    f = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_STORED)
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for filename in filenames:
            f.write(os.path.dirname(dirpath), os.path.join(os.path.basename(dirpath), filename))
    f.close()


if __name__ == '__main__':
    do_zip('/home/data/test/s8_20180502/s8_20180502.zip', '/home/data/test/s8_20180502/cluster/cluster')
