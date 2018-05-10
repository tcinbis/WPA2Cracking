import threading
import subprocess
from subprocess import PIPE
import os
from time import sleep

PATH = os.environ['PATH']
env = {'PATH': PATH, 'MON_PREFIX': 'smoothie'}
aireplay_cmd_template = 'aireplay-ng'


def runAireplay(interface, bssid):
    aireplay_cmd = list()
    aireplay_cmd.append(aireplay_cmd_template)
    aireplay_cmd.append('--deauth')
    aireplay_cmd.append('5')
    aireplay_cmd.append('-a')
    aireplay_cmd.append(bssid)
    aireplay_cmd.append(interface + 'mon')

    aireplay_process = subprocess.Popen(aireplay_cmd, stdout=PIPE, stderr=PIPE, env=env)

    return aireplay_process

class AireplayThread(threading.Thread):
    global process

    def __init__(self, thread_id, interface, bssid):
        super(AireplayThread, self).__init__()
        self._stop_event = threading.Event()
        self.thread_id = thread_id
        self.interface = interface
        self.bssid = bssid
        self.terminated = False

    def run(self):
        global process
        print("Thread {0} starting".format(self.thread_id))
        process = runAireplay(self.interface, self.bssid)

        while (not self._stop_event.is_set()):
            sleep(0.5)
            print("Waiting in thread")

        process.terminate()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set() and self.terminated