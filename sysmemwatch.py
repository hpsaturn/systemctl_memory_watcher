#!/usr/bin/python3
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

def sysCtlPrintBar(scope, state, max):
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
  tics = 10000
  with tqdm(total=bar_max, desc=scope, dynamic_ncols=True, colour=color, bar_format=barf, unit_scale=True) as pbar:
    while i < bar_cur:
      pbar.update(tics)
      i = i+tics

def sysLocalPrintBar(scope, state, max):
  if state*100/max > 35:
    color = "red"
  elif state*100/max > 25:
    color = "yellow"
  else:
    color = "green"

  if stats:
    barf = '{l_bar}{bar:30}{n_fmt}/{total_fmt}'
  else:
    barf = '{l_bar}{bar:50}'

  i = 0
  scope = "{0:>12}".format(scope)
  tics = 100
  with tqdm(total=max, desc=scope, dynamic_ncols=True, colour=color, bar_format=barf, unit_scale=False) as pbar:
    while i < state:
      pbar.update(tics)
      i = i+tics

def sysFanPrintBar(scope, state, max):
  if state <= 2500:
    color = "cyan"
  elif state > 2500 and state <= 2800:
    color = "yellow"
  else:
    color = "red"

  if stats:
    barf = '{l_bar}{bar:30}{n_fmt}/{total_fmt}'
  else:
    barf = '{l_bar}{bar:50}'

  i = 0
  scope = "{0:>12}".format(scope)
  tics = 100
  with tqdm(total=max, desc=scope, dynamic_ncols=True, colour=color, bar_format=barf, unit_scale=False) as pbar:
    while i < state:
      pbar.update(tics)
      i = i+tics

def executePipes(strcur,strmax):
  strvcur = subprocess.check_output(strcur, shell=True)
  strvmax = subprocess.check_output(strmax, shell=True)
  return [strvcur,strvmax]


def sysCtlPrintScopes(scopes):
  for scope in scopes:
    if scope == "fan":
      try:
        fanp = "cat /sys/devices/platform/asus-nb-wmi/hwmon/hwmon6/fan1_input"
        strvcur = subprocess.check_output(fanp, shell=False)
        vcur=int(float(strvcur.split(b'\n')[0]))
      except:
        vcur=0
      valm=9000
      sysFanPrintBar(scope,vcur,valm)
      continue
    memc = "systemctl --user show "+scope + ".scope | grep MemoryCurrent | sed 's/=/ /g' | awk '{print $2}'"
    memx = "systemctl --user show "+scope + ".scope | grep MemoryMax | sed 's/=/ /g' | awk '{print $2}'"
    values = executePipes(memc,memx)
    if values[1] == b'infinity\n':
      memc = "memof "+scope+"| awk '{print $1}'"
      memx = "cat /proc/meminfo | grep MemTotal | awk '{print $2}'"
      values = executePipes(memc,memx)
      imemc=int(float(values[0].split(b'\n')[0]))
      imemx=int(float(values[1].split(b'\n')[0])/1024)
      if imemc > 0 :
        sysLocalPrintBar(scope, imemc, imemx)
      continue
    sysCtlPrintBar(scope, values[0], values[1])


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
        sysCtlPrintScopes(arguments["<scope>"])
        time.sleep(trefresh)
    else:
      sysCtlPrintScopes(arguments["<scope>"])
  except KeyboardInterrupt:
    print("")
