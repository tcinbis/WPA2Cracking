import subprocess
from subprocess import PIPE
import os

class HccapxConverter:
    def __init__(self):
        pass

    def convert(self,captureFileName,outputFileName):
        hashcat_convert_cmd = list()
        hashcat_convert_cmd.append('/usr/lib/hashcat-utils/cap2hccapx.bin '+str(os.path.abspath(captureFileName + '-01.cap'))+' '+outputFileName+'.hccapx')
        hashcat_convert_process = subprocess.Popen(hashcat_convert_cmd, stdout=PIPE, stderr=PIPE, shell=True)

        try:
            outs, errs = hashcat_convert_process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            hashcat_convert_process.kill()
            outs, errs = hashcat_convert_process.communicate()

        err_str = errs.decode('utf-8')
        out_str = outs.decode('utf-8')

        print(out_str)
        print(err_str)

        if hashcat_convert_process.returncode is 0:
            return True
        else:
            return False