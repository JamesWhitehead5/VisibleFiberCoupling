import nidaqmx
from nidaqmx.constants import Edge
from nidaqmx.stream_readers import (
    AnalogSingleChannelReader, AnalogMultiChannelReader)
from nidaqmx.tests.fixtures import x_series_device
import numpy
import matplotlib.pyplot as plt
"""https://nidaqmx-python.readthedocs.io/en/latest/"""

class Daq:
    def __init__(self, number_of_samples, sample_rate):

        read_task = nidaqmx.Task()
        read_task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
        read_task.ai_channels.add_ai_voltage_chan("Dev2/ai1")
        read_task.ai_channels.add_ai_voltage_chan("Dev2/ai2")
        #read_task.in_stream.over_write =  nidaqmx.constants.OverwriteMode.OVERWRITE_UNREAD_SAMPLES

        # read_task.co_channels.add_co_pulse_chan_freq(
        #     '{0}/ctr0'.format(x_series_device.name), freq=sample_rate)
        # read_task.timing.cfg_implicit_timing(
        #     samps_per_chan=number_of_samples)
        #
        # samp_clk_terminal = '/{0}/Ctr0InternalOutput'.format(
        #     x_series_device.name)

        # read_task.timing.cfg_implicit_timing()
        #
        # read_task.timing.cfg_samp_clk_timing(
        #     sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,
        #     samps_per_chan=number_of_samples)

        read_task.timing.cfg_samp_clk_timing(rate=sample_rate, samps_per_chan=number_of_samples)

        # read_task.timing.cfg_samp_clk_timing(
        #     sample_rate, source=samp_clk_terminal,
        #     active_edge=Edge.FALLING, samps_per_chan=number_of_samples)



        self._reader = AnalogMultiChannelReader(read_task.in_stream)
        read_task.start()

        self._task = read_task;

        number_of_channels = 3

        self._values_read = numpy.zeros(
            (number_of_channels, number_of_samples), dtype=numpy.float64)

        self._number_of_samples = number_of_samples


        self._timeout = number_of_samples/sample_rate + 2



    def aquire(self):
        assert self._reader.verify_array_shape, "Preallocated array is the wrong size"

        self._reader.read_many_sample(self._values_read, number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE, timeout=self._timeout)
        #self._reader.read_many_sample(self._values_read, number_of_samples_per_channel=self._number_of_samples, timeout=self._timeout)

        photodiode_voltage, wavelength_voltage, source_voltage = self._values_read[0,:], self._values_read[1,:], self._values_read[2,:]
        #self._task.in_stream.open_chans_exist
        #assert self._task.in_stream.open_chans_exist is False, "Stream is still open"
        self._task.close()
        return photodiode_voltage, wavelength_voltage, source_voltage


def test_manual():
    with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task, nidaqmx.Task() as sample_clk_task:

        # pd_voltage_channel = write_task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
        # wavelength_channel = write_task.ai_channels.add_ai_voltage_chan("Dev2/ai1")

        sample_rate = 1001
        read_task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
        read_task.ai_channels.add_ai_voltage_chan("Dev2/ai1")

        # read_task.timing.cfg_samp_clk_timing(
        #     sample_rate, source=samp_clk_terminal,
        #     active_edge=Edge.FALLING, samps_per_chan=number_of_samples)

        reader = AnalogMultiChannelReader(read_task.in_stream)
        read_task.start()

        number_of_channels = 3
        number_of_samples = 100

        values_read = numpy.zeros(
            (number_of_channels, number_of_samples), dtype=numpy.float64)



        reader.read_many_sample(values_read, number_of_samples_per_channel=number_of_samples, timeout=2)

        print(values_read)
        plt.plot(values_read[0,:], values_read[1,:])
        plt.show()

def test_multiple_aquisitions():
    for _ in range(4):
        d = Daq(number_of_samples=3, sample_rate=1)
        photodiode_voltage, wavelength_voltage, source_voltage = d.aquire()

if __name__ == '__main__':
    test_multiple_aquisitions()
    #test_manual()
    #
    #
    # d = Daq(number_of_samples=101, sample_rate=100)
    # photodiode_voltage, wavelength_voltage, source_voltage = d.aquire()
    #
    # plt.plot(photodiode_voltage, wavelength_voltage)
    # plt.show()
