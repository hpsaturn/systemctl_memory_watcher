#!/usr/bin/python

"""
syswatchmem -- utility for see the memory of each scope launched with systemd-run

Usage:
  syswatchmem  <scope>... 
  syswatchmem [--verbose] [--loop] [--time <delay>] <scope>...
  syswatchmem -h | --help
  syswatchmem -v | --version


Options:
  -l, --loop                    Loop forever
  -t <delay>, --time <delay>    Time between updates [default: 30]
  -h --help                     Show help screen.
  -v --version                  Show version.
  -s, --verbose                 Enable logs

"""


from re import T
from docopt import docopt
import tqdm
from tqdm import tqdm
import subprocess
import os
import time

def printBar(scope, state, max):
  try:
    s = (100*int(state))/int(max)
  except:
    s = 0
  tqdm.write(scope+":")
  for i in tqdm(range(100),position=0, ncols=100, dynamic_ncols=True):
    # time.sleep(0.05)
    if i == int(s):
      break

def printScopes(scopes):
  for scope in scopes:
    # print(scope)
    memc="systemctl --user show "+scope+".scope | grep MemoryCurrent | sed 's/=/ /g' | awk '{print $2}'"
    memx="systemctl --user show "+scope+".scope | grep MemoryMax | sed 's/=/ /g' | awk '{print $2}'"
    mem_cur=subprocess.check_output(memc, shell=True, )
    mem_max=subprocess.check_output(memx, shell=True)
    printBar(scope, mem_cur, mem_max)

if __name__ == '__main__':
  arguments = docopt(__doc__, version='0.0.1')
  debugmode = arguments["--verbose"]
  trefresh = int(arguments["--time"])
  if trefresh < 1:
    trefresh = 30
  print(arguments)
  if arguments["--loop"]:
    while True:
      os.system('cls' if os.name=='nt' else 'clear')
      printScopes(arguments["<scope>"])
      time.sleep(trefresh)
  else: 
    printScopes(arguments["<scope>"])
  