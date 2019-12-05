from nidaqmx.stream_readers import (
    AnalogSingleChannelReader, AnalogMultiChannelReader)
import numpy

# Select a random loopback channel pair on the device.
loopback_channel_pairs = _get_analog_loopback_channels(
    x_series_device)

number_of_channels = random.randint(2, len(loopback_channel_pairs))
channels_to_test = random.sample(
    loopback_channel_pairs, number_of_channels)

with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
    write_task.ao_channels.add_ao_voltage_chan(
        flatten_channel_string(
            [c.output_channel for c in channels_to_test]),
        max_val=10, min_val=-10)

    read_task.ai_channels.add_ai_voltage_chan(
        flatten_channel_string(
            [c.input_channel for c in channels_to_test]),
        max_val=10, min_val=-10)

    writer = AnalogMultiChannelWriter(write_task.out_stream)
    reader = AnalogMultiChannelReader(read_task.in_stream)

    values_to_test = numpy.array(
        [random.uniform(-10, 10) for _ in range(number_of_channels)],
        dtype=numpy.float64)
    writer.write_one_sample(values_to_test)
    time.sleep(0.001)

    values_read = numpy.zeros(number_of_channels, dtype=numpy.float64)
    reader.read_one_sample(values_read)

    numpy.testing.assert_allclose(
        values_read, values_to_test, rtol=0.05, atol=0.005)