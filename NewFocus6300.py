import serial
import time

class NewFocus6300:
    def __init__(self, com_port):
        self._ser = serial.Serial(com_port, 19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                      timeout=0.5)

    def _to_command(self, command: str) ->bytearray:
        return ('@' + command + '\r').encode()

    def _query(self, cmd: str) -> str:
        print()
        print(cmd)
        self._ser.write(self._to_command(cmd))
        #time.sleep(0.05)
        return(self._ser.readline().strip().decode())

    def get_ID(self):
        return self._query("*IDN?")

    def get_wavelength(self):
        return float(self._query(":WAVE?"))

    # def scan_reset(self):
    #     """Stop and return to start wavelength"""
    #     self._query(":OUTPut:SCAN:RESEt")

    def start_scan(self):
        """Start/Restart scan"""
        print(self._query(":OUTPut:SCAN:STARt"))

    def get_power(self):
        """Read front facet power <value mW>"""
        return float(self._query(":SENSe:POWer:LEVel:FRONt"))

    def set_slew_rate_forward(self, rate):
        """Write forward slew-rate set point. (The units are in nm/s.)"""
        print(self._query(":SOURce:WAVElength:SLEWrate:FORWard {}".format(rate)))

    def set_slew_rate_return(self, rate):
        """Write return slew-rate set point. (The units are in nm/s.)"""
        print(self._query(":SOURce:WAVElength:SLEWrate:RETurn {}".format(rate)))

    def set_start_wavelength(self, start_wl):
        """Write scan start-wavelength set point"""
        print(self._query(":SOURce:WAVElength:STARt {}".format(start_wl)))

    def set_stop_wavelength(self, start_wl):
        """Write scan stop-wavelength set point"""
        print(self._query(":SOURce:WAVElength:STOP {}".format(start_wl)))

    def reset_scan(self):
        """The wavelength is reset to the start wavelength at the return slew rate. If a
        scan is in progress it will be interrupted and the wavelength reset to the start
        wavelength. """
        print(self._query(":OUTPut:SCAN:RESEt"))

    def wait_till_complete(self):
        """Sleeps until the laser has finished its operation"""
        print("calls wait till")
        while(not self.is_finished()):
            print(not self.is_finished())
            time.sleep(0.01)

    def set_current(self,cur):
        "set the driving current for the laser"
        print(self._query(":SOURce:CURRent:LEVel:DIODe {}".format(cur)))

    def set_wavlength(self,wl):
        "set the wavelenght of the laser"
        print(self._query(":SOURce:WAVElength {}".format(wl)))


    def is_finished(self):
        return float(self._query("*OPC?")) == 1


    def setup_sweep(self, wl_start, wl_end, forward_speed, reverse_speed):
        """Sweeps the wavelength.
        Wavelengths in nm, speeds in nm/s"""
        self.set_start_wavelength(wl_start)
        self.set_stop_wavelength(wl_end)

        self.set_slew_rate_forward(forward_speed)
        self.set_slew_rate_return(reverse_speed)

        self.reset_scan()
        self.wait_till_complete()


if __name__=='__main__':
    nf = NewFocus6300(com_port='COM4')
    print(nf.get_ID())
    print(nf.get_wavelength())
    nf.set_current(10)
    nf.set_wavlength(638.3)




