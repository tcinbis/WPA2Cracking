from pyrcrack.management import Airmon
from pyrcrack.scanning import Airodump


def main():
    air = Airmon('wlp0s20f0u1')
    # Start interface
    air.start()
    # Setup scanning
    kwargs = {
        'essid_regex': 'UPC*'
    }
    airodump_process = Airodump('wlp0s20f0u1', **kwargs)
    print(airodump_process.clients())


if __name__ == '__main__':
    main()
