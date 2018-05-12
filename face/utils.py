import subprocess


def execute_command(cmd, **kwargs):
    with open('result.log', 'a') as f:
        p = subprocess.Popen(cmd,
                            shell=True,
                            stdout=f.fileno(),
                            stderr=f.fileno(),
                            executable='/bin/bash',
                            **kwargs)
    p.communicate()

    # for line in iter(p.stdout.readline,'b'):
    #     print(line)

    # if p.returncode == 0:
    #     print('Subprogram success')
    # else:
    #     print('Subprogram failed')
