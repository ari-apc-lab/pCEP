#!/usr/local/bin/python

# /*
#  * Copyright (C) 2019  Atos Spain SA. All rights reserved.
#  *
#  * This file is part of pCEP.
#  *
#  * pCEP is free software: you can redistribute it and/or modify it under the
#  * terms of the Apache License, Version 2.0 (the License);
#  *
#  * http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * The software is provided "AS IS", without any warranty of any kind, express or implied,
#  * including but not limited to the warranties of merchantability, fitness for a particular
#  * purpose and noninfringement, in no event shall the authors or copyright holders be
#  * liable for any claim, damages or other liability, whether in action of contract, tort or
#  * otherwise, arising from, out of or in connection with the software or the use or other
#  * dealings in the software.
#  *
#  * See README file for the full disclaimer information and LICENSE file for full license
#  * information in the project root.
#  *
#  * Authors:  Atos Research and Innovation, Atos SPAIN SA
#  */

import pdb

import os, sys                            # get unix, python services
import time
import socket 
import psutil
from glob import glob                     # file name expansion
from os.path import exists                # file exists test
from multiprocessing import Process

##
# It runs the bcep application. Outputs are forwarded to /dev/null to have a clear output
# @param program BCEP executable
# @dolce_file Dolce file to be used in the test
#
def run_program(program, dolce_file, conf_file):
    # 'C:\\Users\\a696457\\dev\\gitlab\\branches\\bcep\\bcep\\x64\\Debug\\bcep.exe -d detect1.dolce -f C:\\Users\\a696457\\dev\\gitlab\\branches\\bcep\\source\\confFile.ini
    os.system(' '.join([program, '-d', dolce_file, '-f', conf_file]))

##
# It receives udp messages from bcep and writes them in a file. It will break when a SHUTDOWN command is received
# @param output_test_file Output file where results are written
#
def receive_udp_messages(output_test_file):
    UDP_IP="127.0.0.1"
    UDP_PORT= 50000
    SHUTDOWN_COMMAND= '7 Shutdown int Result 0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # for Windows allows socket reuse
    sock.bind((UDP_IP,UDP_PORT))
    ofile= open(output_test_file,'a')
    while(True):
        data,addr=sock.recvfrom(1024)
        ofile.write(data)
        if SHUTDOWN_COMMAND in data:
            break

##
# It sends events to BCEP through default UDP socket. After having sent all the commands, it will send a shutdown special event
# @param events Events to be sent to the BCEP
#
def send_udp_message(events):
    UDP_IP="127.0.0.1"
    UDP_PORT= 29654
    SHUTDOWN_MESSAGE="153 Shutdown int scope 0"
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for event in events:
        sock.sendto(event,(UDP_IP,UDP_PORT))
        time.sleep(0.1)	
    sock.sendto(SHUTDOWN_MESSAGE,(UDP_IP,UDP_PORT))

##
# It tests BCEP application considering a specific test environment. The test environment is defined by a dolce file, a test name that is used to store the results and a set of events to be simulated. This function launches three processes: one for the BCEP itself, one to send events through an UDP socker and another to receive the complex events detected and to write them in a file.
# @param program BCEP executable
# @param dolce_file Dolce specification to be used in this specific test
# @param test Test identification
# @param events List of events to be simulated
#
def test_bcep(program, dolce_file, conf_file, test,events):
    p1 = Process(target = run_program, args = (program, '/'.join([testdir, dolce_file]), conf_file))
    # output_file = '.'.join([test, 'out', 'txt'])
    output_file = '.'.join([test, 'out'])
    p2 = Process(target = receive_udp_messages, args = (output_file, ))
    p3 = Process(target = send_udp_message, args = (events, ))
    p1.start()
    p2.start()
    # We need to wait some time so that BCEP is launched completely
    time.sleep(3) 	# Windows is like an old person... needs to sleep more...
    p3.start()
    p2.join()
    # We only wait to the receiver process. When it has finished, we kill the BCEP process and its children and terminate the sender process
    parent = psutil.Process(p1.pid)
    for child in parent.children(recursive = True):
        child.kill()
    # parent.kill()
    p3.terminate

## @package regtest
# This python module aims to perform regression tests to BCEP application. To use it: python regtest.py {path_to_bcep} {path_to_tests_folder}
# @param A command line argument to receive the executable 
# @param A command line argument to receive the tests folder path
#
# The tests folder must contain at least one file with .in extension. In these files, first line defines the name of the dolce file to be used in the test.
# The consequent lines define the list of events to be simulated.
# In the first execution, the script will generate a .out file with the complex events generated. In the consequent executions, results will be compared
# agains this file.
#

print 'RegTest start.' 
print 'path:', os.getcwd(  )              # current directory
print 'time:', time.ctime(), '\n'
program = sys.argv[1]                     # two command-line args
testdir = sys.argv[2]

conf_file = ''
if len(sys.argv) > 3:
    conf_file = sys.argv[3]


def main():

    for test in glob(os.path.join(testdir, '*.in')):      # for all matching input files
        #Test file is read first.
        with open(test) as f:
            content = f.read().splitlines()
        dolce_file = content[0]

        last_out_file = '.'.join([test, 'out', 'last'])
        if exists(last_out_file):
            os.remove(last_out_file)

        if not exists(os.path.join(testdir, dolce_file)):
            print ''.join(['*** FAILED:', test, '(', dolce_file, ' does not exist)'])
        elif not exists('%s.out' % test):
            # no prior results
            test_bcep(program, dolce_file, conf_file, test, content[1:])
            print ''.join(['*** GENERATED:', '%s.out' % test])
        else:
            # pdb.set_trace()

            # backup, run, compare
            output = '.'.join([test, 'out'])
            backup = '.'.join([output, 'bkp'])
            if os.path.exists(backup):
                os.remove(backup)

            os.rename(output, backup)
            test_bcep(program, dolce_file, conf_file, test, content[1:])
            
            # pdb.set_trace()

            diff_file = '.'.join([test, 'diffs'])

            if os.path.exists(diff_file):
                os.remove(diff_file)
                        
            os.system('FC %s.out %s.out.bkp > %s.diffs' % ((test, )*3) )

            df = open(diff_file)
            
            # if os.stat(diff_file)[ST_SIZE] == 0:
            if 'FC: no differences encountered' in df.read():
                print ''.join(['*** PASSED:', test])
                # os.remove(diff_file)
            else:
                print ''.join(['*** FAILED:', test, '(see ', test, '.diffs)'])
                
                os.rename('.'.join([test, 'out']), '.'.join([test, 'out', 'last']))
                os.rename('.'.join([test, 'out', 'bkp']), '.'.join([test, 'out']))
    
    print 'RegTest done:', time.ctime()


if __name__ == '__main__':
    # freeze_support()
    main()
