"""
syswatchmem -- utility for see the memory of each scope launched with systemd-run

Usage:
  syswatchmem  <scope>... 
  syswatchmem [--verbose] <scope>...
  syswatchmem -h | --help
  syswatchmem -v | --version


Options:
  -h --help                     Show help screen.
  -v --version                  Show version.
  -s, --verbose                 Enable logs
"""


import time
import tqdm
from docopt import docopt
import os

from tqdm import tqdm


if __name__ == '__main__':
  arguments = docopt(__doc__, version='0.0.1')
  debugmode = arguments["--verbose"]
  for i in tqdm(range(10)):
    time.sleep(0.1)