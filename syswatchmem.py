#!/usr/bin/python

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
import subprocess
from tqdm import tqdm


def printBar(scope, state, max):
  try:
    s = (100*int(state))/int(max)
  except:
    s = 0
  # for i in tqdm(range(100),position=0,miniters=int(1e6),desc=scope+"\t", dynamic_ncols=True):
  tqdm.write(scope+":")
  for i in tqdm(range(100),position=0, ncols=100):
    # time.sleep(0.05)
    if i == int(s):
      break

if __name__ == '__main__':
  arguments = docopt(__doc__, version='0.0.1')
  debugmode = arguments["--verbose"]
  # print(arguments)
  for scope in arguments["<scope>"]:
    # print(scope)
    memc="systemctl --user show "+scope+".scope | grep MemoryCurrent | sed 's/=/ /g' | awk '{print $2}'"
    memx="systemctl --user show "+scope+".scope | grep MemoryMax | sed 's/=/ /g' | awk '{print $2}'"
    mem_cur=subprocess.check_output(memc, shell=True, )
    mem_max=subprocess.check_output(memx, shell=True)
    printBar(scope, mem_cur, mem_max)

