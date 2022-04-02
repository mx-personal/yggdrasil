import subprocess
from yggdrasil.logger import logger


class CmdError(Exception):
    def __init__(self, error: str):
        self.message = 'Aborting, error in commands communicated:\n{0}'.format(error)
        super().__init__(self.message)


def run_cmds(cmds:[]):
    for cmd in cmds:
        output = subprocess.run(cmd, shell=True, check=False, capture_output=True)
        logger.debug("command output:{0}".format(output.stdout.decode("utf-8")))
        logger.debug("return code: {0}".format(output.returncode))
        if output.returncode != 0:
            raise CmdError(output.stderr.decode("utf-8"))


def generate_custom_batch(source: str, destination: str, replacements: []):
    # Generate batch launcher
    with open(source) as f:
        batch = f.readlines()
    for i, row in enumerate(batch):
        for find, repl in replacements:
            row = row.replace(find, repl)
            batch[i] = row
    with open(destination, 'w+') as f:
        f.write("".join(batch))
