#!/usr/bin/python

"""
syswatchmem -- utility for see the memory of each scope launched with systemd-run

Usage:
  syswatchmem  <scope>... 
  syswatchmem [--verbose] [--loop] [--time <delay>] [--div <div>] <scope>...
  syswatchmem -h | --help
  syswatchmem -v | --version


Options:
  -l, --loop                    Loop forever
  -t <delay>, --time <delay>    Time between updates [default: 30]
  -d <div>, --div <div>         Divisor of memory [default: 1000] Mbytes
  -h --help                     Show help screen.
  -v --version                  Show version.
  -s, --verbose                 Enable logs
"""

from docopt import docopt
import tqdm
from tqdm import tqdm
import subprocess
import os
import time

div=1000

def printBar(scope, state, max):
  try:
    bar_max = int(int(max)/div)
    bar_cur = int(int(state)/div)
  except:
    bar_max = 100
    bar_cur = 0
  if bar_cur*100/bar_max > 80:
    color="red"
  elif bar_cur*100/bar_max > 50:
    color="yellow"
  else:
    color="green"
  for i in tqdm(range(bar_max),desc="{0:>8}".format(scope), position=0, ncols=100, dynamic_ncols=True,colour=color):
    if i == bar_cur:
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
  try:
    arguments = docopt(__doc__, version='0.0.1')
    debugmode = arguments["--verbose"]
    trefresh = int(arguments["--time"])
    div = int(arguments["--div"])
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
  except KeyboardInterrupt:
    print("")
  