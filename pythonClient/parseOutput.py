import csv
import os
from os import path
from pandas import read_csv


class AiroParser:

    def __init__(self, outputFile):
        if path.exists('tmp0'):
            os.remove('tmp0')
        if path.exists('tmp1'):
            os.remove('tmp1')

        self.output = outputFile

    def splitCsvFile(self):
        with open(self.output, 'r') as myfile:
            data = myfile.read().replace(' ', '').split('\n\n')

        files = list()
        for idx, tmp in enumerate(data):
            if tmp is not "":
                file = open('tmp{}'.format(idx), 'w')
                file.writelines(tmp)
                file.close()
                files.append(open('tmp{}'.format(idx), 'r'))
        return files

    def pandaParse(self):
        files = self.splitCsvFile()
        dfBssid = read_csv(files[0], header=0, sep=',')
        dfClients = read_csv(files[1], header=0, sep=',')

        self.available_bssids = dfBssid['BSSID'].tolist()
        self.available_ESSID = dfBssid['ESSID'].tolist()
        self.available_channels = dfBssid['channel'].tolist()

    def parse(self):
        files = self.splitCsvFile()

        with open(files[0].name, newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)

    def get_bssids(self):
        return self.available_bssids

    def get_channels(self):
        return self.available_channels


def main():
    pars = AiroParser('output-D77B0-01.csv')
    pars.pandaParse()


if __name__ == '__main__':
    main()
