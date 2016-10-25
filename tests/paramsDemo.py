#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

CMD_T = 'AB010105'
CMD_H = 'AB020105'
CMD_Q = 'AB030101'

CMD_T_STOP = 'AB0100'
CMD_H_STOP = 'AB0200'
CMD_Q_STOP = 'AB0300'

init_cmds = [CMD_T_STOP, CMD_H_STOP, CMD_Q_STOP, CMD_T, CMD_H, CMD_Q]

parser = argparse.ArgumentParser(description='For example AB0100,AB0200,AB0200,AB010105,AB020105,AB030101')
parser.add_argument('-c', '--cmds', help='delimited list input', type=str)
args = parser.parse_args()

if args.cmds is None:
    args.cmds = ''
print(args)

params_cmds_list = args.cmds.upper().split(',')

if params_cmds_list != ['']:
    init_cmds = params_cmds_list

print(init_cmds)
