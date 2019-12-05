import serial
import time

class NewFocus6300:
    def __init__(self, com_port='COM3'):
        self._ser = serial.Serial(com_port, 19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                      timeout=0.5)

    def _to_command(self, command: str) ->bytearray:
        return ('@' + command + '\r').encode()

    def _query(self, cmd: str) -> str:
        self._ser.write(self._to_command(cmd))
        time.sleep(0.05)
        return(self._ser.readline().strip().decode())

    def get_ID(self):
        return self._query("*IDN?")

    def get_wavelength(self):
        return float(self._query(":WAVE?"))

if __name__=='__main__':
    nf = NewFocus6300()
    print(nf.get_ID())
    print(nf.get_wavelength())
