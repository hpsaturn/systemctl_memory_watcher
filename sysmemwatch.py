#!/usr/bin/python
# This file is part of the sysmemwatch:
# https://github.com/hpsaturn/systemctl_memory_watcher
# Copyright (c) 2022, @hpsaturn, Antonio Vanegas
# https://hpsaturn.com, All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
syswatchmem -- utility for see the memory of each scope launched with systemd-run

Usage:
  syswatchmem  <scope>... 
  syswatchmem [--loop] [--no-stats] [--anim <tics>] [--time <delay>] <scope>...
  syswatchmem -h | --help
  syswatchmem -v | --version

Examples:
  syswatchmem -n firefox                # watch the memory of firefox one time without stats only %
  syswatchmem -l -t 60 firefox vscode   # loop mode: watch the memory of firefox and vscode each 60 seconds
  syswatchmem -a 5000 firefox vscode    # animate more the memory bars (minus is more slow)

Options:
  -l, --loop                    Loop forever
  -t <delay>, --time <delay>    Time between updates [default: 30] seconds
  -a <tics>, --anim <tics>      Anim speed [default: 10000] minus is slower
  -n, --no-stats                Disable statistics
  -h --help                     Show help screen.
  -v --version                  Show version.
"""

from docopt import docopt
import tqdm
from tqdm import tqdm
import subprocess
import os
import time

stats = True
tics = 10000

def printBar(scope, state, max):
  try:
    bar_max = int(int(max))
    bar_cur = int(int(state))
  except:
    bar_max = 10E9
    bar_cur = 0
  if bar_cur*100/bar_max > 80:
    color = "red"
  elif bar_cur*100/bar_max > 50:
    color = "yellow"
  else:
    color = "green"

  if stats:
    barf = '{l_bar}{bar:30}{n_fmt}/{total_fmt}'
  else:
    barf = '{l_bar}{bar:50}'

  i = 0
  scope = "{0:>12}".format(scope)
  with tqdm(total=bar_max, desc=scope, dynamic_ncols=True, colour=color, bar_format=barf, unit_scale=True) as pbar:
    while i < bar_cur:
      pbar.update(tics)
      i = i+tics


def printScopes(scopes):
  for scope in scopes:
    memc = "systemctl --user show "+scope + ".scope | grep MemoryCurrent | sed 's/=/ /g' | awk '{print $2}'"
    memx = "systemctl --user show "+scope + ".scope | grep MemoryMax | sed 's/=/ /g' | awk '{print $2}'"
    mem_cur = subprocess.check_output(memc, shell=True, )
    mem_max = subprocess.check_output(memx, shell=True)
    printBar(scope, mem_cur, mem_max)


if __name__ == '__main__':
  try:
    arguments = docopt(__doc__, version='0.0.1')
    trefresh = int(arguments["--time"])
    stats = arguments["--no-stats"] == False
    tics = int(arguments["--anim"])
    if trefresh < 1:
      trefresh = 30
    if arguments["--loop"]:
      while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        printScopes(arguments["<scope>"])
        time.sleep(trefresh)
    else:
      printScopes(arguments["<scope>"])
  except KeyboardInterrupt:
    print("")
