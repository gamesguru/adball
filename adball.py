#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 20:18:29 2018

@author: shane
"""

import os, sys
import subprocess, threading
import shlex

#Command execution function `cmd()`
def cmd(cmds, _cwd='', selfdebug=True):
    if _cwd == '':
        _cwd = os.getcwd()
    try:
        if selfdebug:
            print(cmds)
        _output = subprocess.check_output(cmds, stderr=subprocess.STDOUT, shell=True, cwd=_cwd, encoding='850')
        if selfdebug:
            print(wrap(cmds, '#'))
            print(_output)
        return _output.splitlines()
    except subprocess.CalledProcessError as e:
        _output = e.output
        print(cmds)
        print(_output)
        return _output.splitlines()

#Get a list of attached serials
def currently_attached_serials():
    serials = []
    for line in cmd('adb devices'):
        if '\tdevice' in line:
            serials.append(line.split('\t')[0])
    print(f'You have {len(serials)} attached devices!!\n\n')
    return serials

def wrap(input, wrapper_char):
    bar = ''
    for i in range(0, len(input) + 6):
        bar += wrapper_char
    return f'{bar}\n## {input} ##\n{bar}'

####################
## MAIN FUNCTION ###
####################
args = []
n = 0
for arg in sys.argv:
    if n == 0:
        n += 1
        continue
    args.append(arg)
cmds = ' '.join(args)
threads = []
print('==> GATHER DEVICES\n')
for serial in currently_attached_serials():
    t = threading.Thread(target=cmd, args=(f'adb -s {serial} {cmds}',))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print('==> FINISHED')
