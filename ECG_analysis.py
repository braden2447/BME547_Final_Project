import json
import math
import logging
from biosppy.signals import ecg
import matplotlib.pyplot as plt


def read_data(filename):
    """Read in patient data from ECG test data file

    An ECG, or electrocardiogram, records the electrical signals
    of the heart to diagnose a variety of heart problems, including
    arrythmias and previous heart attacks.  Raw ECG data must be
    filtered to remove background noise before it is analyzed by
    a cardiologist.  More info on ECGs can be found at:
    https://www.webmd.com/heart-disease/electrocardiogram-ekgs

    :param filename: string containing name of input test file

    :returns: string containing all ECG test data from input file
    """
    test = open(filename, 'r')
    test_data = test.read()
    test.close()
    # logging.info('Beginning analysis of new ECG trace using {}'.format(
    # filename.replace('test_data/', '')))
    return test_data


def manipulate_data(data):
    """Split input text string into voltage and time lists, logging data errors

    The input data is first split by line return characters to sort data into
    a list of time, voltage pairs. This data is then split by commas to
    separate the time and voltage values into individual list items. From this
    point, the values are analyzed to log and skip over invalid data and append
    valid data to separate time and voltage lists.

    :param data: string containing all ECG test data

    :returns:
        - time - list containing ECG test time values
        - voltage - list containing ECG test voltage values
    """
    line_split = data.split('\n')
    comma_split = []
    for i in line_split:
        comma_split.append(i.split(','))
    comma_split.pop()
    time = []
    voltage = []
    for x in comma_split:
        try:
            num = [float(y) for y in x]
            if math.isnan(num[0]) or math.isnan(num[1]) is True:
                logging.warning('NaN value found and skipped.')
            else:
                time.append(num[0])
                voltage.append(num[1])
        except ValueError:
            logging.warning('Tried to convert non-numeric to float. Data pair'
                            ' skipped.')
    return time, voltage


def warning(voltage):
    """Create a warning-level entry for abnormally large voltage values

    The voltage data list is iterated through to test if any of the values
    exceed the normal range of +/- 300 mV.

    :param voltage: list containing ECG test voltage values
    :param filename: string containing name of input test file

    :returns: None
    """
    warn = any(abs(val) > 300 for val in voltage)
    if warn is True:
        logging.warning('Voltages found in this file have exceeded the'
                        ' normal range of +/- 300 mV.')

    return


def time_volt_calcs(time, voltage):
    """Evaluate ECG test duration and calculate max/min voltage values

    The ECG test duration is evaluating by picking out the last time value
    in the time list. The python functions min() and max() are used to
    identify the minimum and maximum voltage values, respectively, from the
    voltage list. These values are appended to a new list variable called
    metrics.

    :param time: list containing ECG test time values
    :param voltage: list containing ECG test voltage values

    :returns: list containing time duration value as a float and min/max
              voltage values as a tuple
    """
    metrics = []
    duration = time[-1]
    metrics.append(duration)
    logging.info('Calculating ECG time duration to be labeled "duration"')
    voltage_extremes = (min(voltage), max(voltage))
    metrics.append(voltage_extremes)
    logging.info('Calculating voltage min and max values to be labeled'
                 ' "voltage_extremes"')
    return metrics


def filter_data(time, voltage, metrics):
    """Filter and evaluate specific ECG test characteristics

    The Python toolbox BioSPPy, Biosignal Processing in Python, is imported and
    used to filter the raw ECG data and provide important ECG characteristics
    such as R-peak locations, heart rate, and heart beats. This package also
    provides a useful graph to visually analyze the raw vs. filtered ECG data.
    This package and its specifications can be found at:
    https://biosppy.readthedocs.io/en/stable/index.html

    :param time: list containing ECG test time values
    :param voltage: list containing ECG test voltage values
    :param metrics: list containing time duration and min/max voltage values

    :returns: list of metrics with appended values for number of heart beats,
              mean heart rate, and heart beat times
    """
    volt_filtered = ecg.ecg(signal=voltage,
                            sampling_rate=(len(time)/time[-1]),
                            path=(r"ecg_data.png"),
                            show=False)

    # Matplotlib plot for final project
    plt.clf()
    plt.plot(volt_filtered[0], volt_filtered[1])
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('ECG Trace')
    plt.savefig("ecg_trace.jpg")

    num_beats = len(volt_filtered[2])  # Num of heartbeats using rpeaks array
    metrics.append(num_beats)
    logging.info('Calculating number of heart beats to be labeled "num_beats"')
    mean_hr_bpm = num_beats/time[-1]*60  # Mean bpm
    mean_hr_bpm = round(mean_hr_bpm)
    metrics.append(mean_hr_bpm)
    logging.info('Calculating average heart rate to be labeled "mean_hr_bpm"')
    beats = []
    for val in volt_filtered[2]:
        beats.append(time[val])  # Beat times based off rpeak index values
    metrics.append(beats)
    logging.info('Calculating heart beat times to be labeled "beats"')
    return metrics


def metrics_dict(data_list):
    """Organize calculated ECG data into a dictionary

    The ECG test characteristics of concern are extracted from the metrics
    list and organized into a dictionary to make the data more readable
    and easier to navigate.

    :param data_list: list of ECG metrics

    :returns: dictionary of metrics containing the keywords: 'duration',
              'voltage_extremes', 'num_beats', 'mean_hr_bpm', and 'beats'
    """
    metrics_dict = {'duration': data_list[0],
                    'voltage_extremes': data_list[1],
                    'num_beats': data_list[2],
                    'mean_hr_bpm': data_list[3],
                    'beats': data_list[4]
                    }
    return metrics_dict


def output_json(metrics, filename):
    """Output ECG metrics to specified json file

    The specific ECG test data metric dictionary is output to a json
    file with the same name as the test data .csv file.

    :param metrics: dictionary of calculated ECG metrics
    :param filename: string containing name of input test file

    :returns: json file of ECG metrics to local disk
    """
    filename = filename.replace('.csv', '')
    out_file = open('{}.json'.format(filename), 'w')
    json.dump(metrics, out_file)
    out_file.close


if __name__ == '__main__':
    logging.basicConfig(filename='ECG_test_log.log',
                        filemode='w', level=logging.INFO)
    test_file = 'test_data1.csv'
    ecg_data = read_data('test_data/' + test_file)
    time, voltage = manipulate_data(ecg_data)
    warning(voltage)
    metrics = time_volt_calcs(time, voltage)
    filtered_metrics = filter_data(time, voltage, metrics)
    metrics_dict = metrics_dict(filtered_metrics)
    output_json(metrics_dict, test_file)
