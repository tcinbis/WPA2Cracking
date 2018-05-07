from time import sleep
import os
import subprocess
from subprocess import PIPE
import threading
import _thread

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

def runAirodump(interface,args):
    airodump_cmd = list()
    airodump_cmd.append(airodump_cmd_template)
    for arg in args:
        airodump_cmd.append(arg)
    airodump_cmd.append(interface+'mon')

    print(airodump_cmd)

    airmon_process = subprocess.Popen(airodump_cmd, stdout=PIPE, stderr=PIPE, env=env)

    return airmon_process

class AirodumpThread (threading.Thread):
    global process

    def __init__(self,thread_id, interface, arg_list):
        super(AirodumpThread, self).__init__()
        self._stop_event = threading.Event()
        self.thread_id = thread_id
        self.interface = interface
        self.arg_list = arg_list

    def run(self):
        global process
        print("Thread {0} starting".format(self.thread_id))
        process = runAirodump(self.interface,self.arg_list)

        while(not self._stop_event.is_set()):
            sleep(0.5)
            print("Waiting in thread")

        process.terminate()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def main():
    interface = 'wlan0'
    if startInterface(interface):
        # continue, because airmon was successful
        arg_list = list()
        arg_list.append('--write')
        arg_list.append('output')
        arg_list.append('--output-format')
        arg_list.append('csv')

        thread1 = AirodumpThread(1,interface,arg_list)
        thread1.setDaemon(True)
        thread1.start()
        #process = runAirodump(interface,arg_list)
    else:
        return -1

    sleep(5)
    print("Send stop to thread")
    thread1.stop()
    print("Asked thread to stop now.")
    sleep(1)
    print(thread1.isAlive())


if __name__ == '__main__':
    main()
