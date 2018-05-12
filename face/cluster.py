import utils


def do_cluster():
    cmd = './run_and_zip'
    utils.execute_command(cmd, **{'cwd': '/home/z00355208/proc_data_pro'})


if __name__ == '__main__':
    do_cluster()
