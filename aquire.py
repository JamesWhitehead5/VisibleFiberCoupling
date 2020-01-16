import time

import numpy as np
import matplotlib.pyplot as plt
from fileutils import query_yes_no, ensure_no_overwrite
import os


from NewFocus6300 import NewFocus6300
from NIDAQ import Daq

def getspectrum():
    #Connect to laser and setup sweep
    nf = NewFocus6300(com_port='COM4')

    #wl_center = 637.0
    #wl_width = 640.0

    wl_start = 637.0
    wl_end = 640.0

    # wl_start = 637
    # wl_end = 637.5
    sweep_rate = 0.1 #0.1
    nf.setup_sweep(wl_start=wl_start, wl_end=wl_end, forward_speed=sweep_rate, reverse_speed=10)

    #Connect to DAQ. Setup DAC aquisition
    estimated_time = (wl_end - wl_start)/sweep_rate
    desired_points = 1000
    dac = Daq(number_of_samples=desired_points, sample_rate=desired_points/estimated_time)

    #Time estimate
    print("About to start sweep. Should take {} seconds.\n Started at {}.".format(estimated_time, time.time()))

    #start sweep
    print("Starting sweep...")
    nf.start_scan()


    #Start aquisition
    print("Starting aqusition")
    photodiode_voltage, wavelength_voltage, source_voltage = dac.aquire()
    dac.close()

    #TODO: Calibrate voltage. Currently incorrect: Assumes that both sweep and aqusition start instantly.
    wavelength = np.linspace(wl_start, wl_end, desired_points)

    #Plot pretty
    plt.plot(wavelength, photodiode_voltage/source_voltage)
    plt.xlabel('Wavelength(nm)')
    plt.ylabel('Intensity (a.u.)')
    plt.show()

    #plt.plot(wavelength, source_voltage )
    #plt.xlabel('Wavelength(nm)')
    #plt.ylabel('Intensity (a.u.)')
    #plt.show()

    #Save file
    if query_yes_no(question="Do you want to save?", default='yes'):
        while True :
            filename = input("What name do you want to give the data?")
            if os.path.exists(filename):
                print("The filename selected already exists. Please either delete existing file or choose a different name.")
            else:
                break

        np.savetxt(filename, (wavelength_voltage, photodiode_voltage, source_voltage))

def powerSeries():
    #Connect to laser and setup sweep
    nf = NewFocus6300(com_port='COM4')

    #set wavelength
    wl = 638.1
    nf.set_wavlength(wl)

    #Connect to DAQ. Setup DAC aquisition
    desired_points = 50
    timeperiod = 5.0

    #set driven curr

    cur_start = 40.0
    cur_end = 50.0
    num_cur = 3

    curr = np.linspace(cur_start,cur_end,num_cur)

    photodiode_voltage_array = np.zeros((num_cur, desired_points))
    wavelength_voltage_array = np.zeros((num_cur, desired_points))
    source_voltage_array = np.zeros((num_cur, desired_points))



    for i in range(num_cur):
        dac = Daq(number_of_samples=desired_points, sample_rate=desired_points / timeperiod)
        nf.set_current(curr[i])
        time.sleep(2.0)

        output = dac.aquire()
        photodiode_voltage, wavelength_voltage, source_voltage = output

        photodiode_voltage_array[i,:] = photodiode_voltage
        wavelength_voltage_array[i,:] = wavelength_voltage
        source_voltage_array[i,:] = source_voltage


        print(source_voltage)

        #wavelength_voltage[i,:] = wavelength_voltage
        #source_voltage[i,:] = source_voltage

    #print(source_voltage_array[0, :])
    #print(source_voltage_array[1, :])
    #print(source_voltage_array[2, :])

    #plt.xlabel('Wavelength(nm)')
    #plt.ylabel('Intensity (a.u.)')
    #plt.show()


    if query_yes_no(question="Do you want to save?", default='yes'):
        while True:
            filename = input("What name do you want to give the data?")
            if os.path.exists(filename):
                print(
                    "The filename selected already exists. Please either delete existing file or choose a different name.")
            else:
                break

        np.savetxt(filename, (wavelength_voltage, photodiode_voltage, source_voltage))


if __name__ == '__main__':
    #getspectrum()
    powerSeries()