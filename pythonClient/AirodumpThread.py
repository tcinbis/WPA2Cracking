import os
import subprocess
import threading
from time import sleep
from subprocess import PIPE

airodump_cmd_template = 'airodump-ng'
PATH = os.environ['PATH']
env = {'PATH': PATH, 'MON_PREFIX': 'smoothie'}

def runAirodump(interface, args):
    airodump_cmd = list()
    airodump_cmd.append(airodump_cmd_template)
    for arg in args:
        airodump_cmd.append(arg)
    airodump_cmd.append(interface + 'mon')

    print(airodump_cmd)

    airmon_process = subprocess.Popen(airodump_cmd, stdout=PIPE, stderr=PIPE, env=env)

    return airmon_process


class AirodumpThread(threading.Thread):
    global process

    def __init__(self, thread_id, interface, arg_list):
        super(AirodumpThread, self).__init__()
        self._stop_event = threading.Event()
        self.thread_id = thread_id
        self.interface = interface
        self.arg_list = arg_list
        self.terminated = False

    def run(self):
        global process
        print("Thread {0} starting".format(self.thread_id))
        process = runAirodump(self.interface, self.arg_list)

        while (not self._stop_event.is_set()):
            sleep(0.5)
            print("Waiting in thread")

        process.terminate()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set() and self.terminated