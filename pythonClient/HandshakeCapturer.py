from time import sleep
import os
import subprocess
from subprocess import PIPE

airmon_cmd_template = 'airmon-ng'
airodump_cmd_template = 'airodump-ng'
PATH = os.environ['PATH']
env = {'PATH': PATH, 'MON_PREFIX': 'smoothie'}

def startInterface(interface):
    airmon_cmd = list()
    airmon_cmd.append(airmon_cmd_template)
    airmon_cmd.append('start')
    airmon_cmd.append(interface)

    print(airmon_cmd)

    airmon_process = subprocess.Popen(airmon_cmd,stdout=PIPE, stderr=PIPE,env=env)

    try:
        outs, errs = airmon_process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        airmon_process.kill()
        outs, errs = airmon_process.communicate()

    err_str = errs.decode('utf-8')
    out_str = outs.decode('utf-8')

    print(out_str)

    interface_success = interface+'mon'

    if interface_success in out_str:
        return True
    else:
        return False

def stopInterface(interface):
    interface = interface+'mon'
    airmon_cmd = list()
    airmon_cmd.append(airmon_cmd_template)
    airmon_cmd.append('stop')
    airmon_cmd.append(interface)

    airmon_process = subprocess.Popen(airmon_cmd,stdout=PIPE, stderr=PIPE,env=env)

    try:
        outs, errs = airmon_process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        airmon_process.kill()
        outs, errs = airmon_process.communicate()

    err_str = errs.decode('ascii')
    out_str = outs.decode('ascii')

    print(out_str)

    interface_success = interface

    if interface_success in out_str:
        return True
    else:
        return False

def main():
    print(startInterface('wlan0'))
    sleep(5)
    print(stopInterface('wlan0'))
    #airodump_process = Airodump('wlan0mon',**kwargs)
    #airodump_process._flags = ['--write', 'output']
    #airodump_process.start()
    #print(airodump_process.writepath)
    #sleep(5)
    #print(airodump_process.stop())
    #print(airodump_process.clients())


if __name__ == '__main__':
    main()
