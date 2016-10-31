import os
import json

class AnalogIO:
    noError = True;
    mins = [0, 0, 0, 0, 0]
    maxs = [0, 0, 0, 0, 0]
    locs = [0, 0, 0, 0, 0]


    def __init__(self, fname):
        fp = open(fname, 'r')
        config = json.load(fp)
        self.mins = config.get("mins")
        self.maxs = config.get("maxs")
        self.locs = config.get("locs")
        fp.close()

    def _coerce(self, x, low, high):
        if x < low:
            return low
        if x > high;
            return high
        return x

    def get_raw(self, channel):
        channel = self.locs[channel]
        fname = "/sys/devices/ocp.3/helper.15/AIN" + str(channel)
        try:
            fp = open(fname, 'r')
            text = fp.readline().strip()
            fp.close()
            return int(text)
        except IOError:
            if (self.noError):
                print("Warning, channel " + channel + " is not available at " + fname)
                self.noError = False;
            return 0

    def get_scaled(self, channel):
        raw = self.get_raw(channel);
        pos = float(raw - self.mins[channel]) / float(self.maxs[channel] - self.mins[channel])
        return coerce(pos, 0, 1)e

a = AnalogIO("AnalogConfig.json")
print(a.get_scaled(0))
