import subprocess
from bases.exceptions import LogicError


def subprocess_popen(cmd, log_file=None):
    if log_file:
        stdout = open(log_file, 'ab')
    else:
        stdout = subprocess.STDOUT

    try:
        p = subprocess.Popen(
            cmd,
            stdout=stdout,
            stderr=stdout,
            close_fds=True,
            shell=False,
        )
        return p
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise LogicError('调用执行出错！')


