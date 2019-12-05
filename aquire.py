import time

import numpy as np
import matplotlib.pyplot as plt

from NewFocus6300 import NewFocus6300
from NIDAQ import Daq

def main():
    #Connect to laser and setup sweep
    nf = NewFocus6300(com_port='COM3')
    wl_start = 637
    wl_end = 640
    sweep_rate = 0.1
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
    photodiode_voltage, wavelength_voltage = dac.aquire()
    dac.close()

    #TODO: Calibrate voltage. Currently incorrect: Assumes that both sweep and aqusition start instantly.
    wavelength = np.linspace(wl_start, wl_end, desired_points)

    #Plot pretty
    plt.plot(wavelength, photodiode_voltage, )
    plt.xlabel('Wavelength(nm)')
    plt.ylabel('Intensity (a.u.)')
    plt.show()





if __name__ == '__main__':
    main()