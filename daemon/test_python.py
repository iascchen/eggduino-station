#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import argparse
from time import time, sleep
import thread

##########################
# Parse input params
##########################

parser = argparse.ArgumentParser(
    description='Example : AB0100,AB0200,AB0300,AB0400,AB01010f,AB020105,AB03010384,AB040105')
parser.add_argument('-c', '--cmds', help='delimited list input', type=str)
args = parser.parse_args()

if args.cmds is None:
    args.cmds = ''
# print(args)

params_cmds_list = args.cmds.upper().split(',')

print "Run Python"
globvar = 1


def show_data():
    while True:
        global globvar
        globvar += 1
        print "thread", globvar, '\n'
        sleep(1)


if params_cmds_list != ['']:
    print "-".join(params_cmds_list)
    print "Daemon"
    thread.start_new_thread(show_data, ())

    while True:
        print "main", globvar, '\n'
        sleep(1)


else:
    print "Process"
