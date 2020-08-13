import logging
import numpy
import matplotlib.pyplot as plt
import time

from Tracker import Tracker
from datetime import datetime


logger = logging.getLogger(__name__)
# Data shown on the plot represents the last 1 minutes
DATA_DURATION = 10
# The data variable
speeds_recv = []
speeds_sent = []
times = []

def main():
    """ Executes the program.
    """
    tracker = Tracker()
    plt.ion()
    last_total_data_used = 0

    while True:
        # Retrieve the up and down speeds
        time.sleep(0.5)
        down_speed = 8 * (tracker.get_current_download_speed() / (2**20))
        up_speed = 8 * (tracker.get_current_upload_speed() / (2**20))

        # Store it
        add_data(down_speed, up_speed)

        # Data used
        total_data_used = round(tracker.get_total_data_used() / (2**20), 3)
        write_data_used(last_total_data_used, total_data_used)
        last_total_data_used = total_data_used

        # Update & display the plot
        recv_curve, = plt.plot(times, speeds_recv)
        sent_curve, = plt.plot(times, speeds_sent)

        plt.legend([recv_curve, sent_curve], ['Download', 'Upload'])
        plt.ylabel('Mb/s', fontsize=8)
        ax = plt.gca()
        ax.tick_params(axis='x', labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        ax.get_figure().canvas.set_window_title('Internet speed - Vishrut')

        plt.draw()
        plt.pause(0.0001)
        plt.clf()


def add_data(down_speed, up_speed):
    if len(times) > 1:
        if divmod((times[-1] - times[0]).total_seconds(), 60)[0] >= DATA_DURATION:
            del times[0]
            del speeds_recv[0]
            del speeds_sent[0]
    speeds_recv.append(down_speed)
    speeds_sent.append(up_speed)
    times.append(datetime.now())


def write_data_used(last_total_data_used, total_data_used):
    if total_data_used != last_total_data_used:
        if total_data_used > last_total_data_used + 0.5:
            print('!! ' + str(total_data_used) + ' Mo used.')
        elif total_data_used > last_total_data_used + 1:
            print('! ' + str(total_data_used) + ' Mo used.')
        else:
            print(str(total_data_used) + ' Mo used.')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s ' +
                                  '-- %(levelname)s ' +
                                  '-- [%(filename)s:%(lineno)s ' +
                                  '-- %(funcName)s() ] ' +
                                  '-- %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        main()
    except Exception as e:
        logger.exception('Unexpected error')

