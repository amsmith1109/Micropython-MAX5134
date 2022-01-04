import ustruct
import time

_CLR            =   b'\x02\xff\xff'
_LDAC           =   0x01
_POWER_CONTROL  =   0x03
_LINEARITY      =   b'\x05\x02\x00'
_WRITE          =   0x10
_WRITE_THROUGH  =   0x30

class MAX5134:
    def __init__(self, CS, SPI, max=None):
        if max is None:
            max = 5 #Assumes a default of 5 V max
        self.cs = CS
        self.spi = SPI
        self.max = max
        self.power = 1

    def v2b(self, voltage):
        if voltage >= self.max: #Handles rollover
            val = 2**16-1
            print('Input set to max.')
        elif voltage < 0: #Handles rollover (again)
            val = 0
            print('Input is negative. Setting to zero.')
        else:
            val = int(round(voltage * 2 ** 16 / self.max))
        return val

    def write(self, channel, voltage):
        channel_word = self.channel_word(channel)
        select = _WRITE_THROUGH + channel_word
        val = self.v2b(voltage)
        stream = ustruct.pack('>BH', select, val)
        self.push(stream)

    def load(self, channel, voltage):
        channel_word = self.channel_word(channel)
        select = _WRITE + channel_word
        val = self.v2b(voltage)
        stream = ustruct.pack('>BH', select, val)
        self.push(stream)

    def clear(self):
        print('Clearing DAC registers.')
        self.push(_CLR)

    def linearity(self):
        self.push(_LINEARITY)

    def ldac(self, channel):
        channel_word = self.channel_word(channel)
        stream = ustruct.pack('>BBB', _LDAC, channel_word, 0xff)
        self.push(stream)

    def pwr(self, channel):
        channel_word = self.channel_word(channel)
        if self.power == 1:
            set = 0xef
            self.power = 0
            print('Powering Off.')
        stream = ustruct.pack('>BBB', _POWER_CONTROL, channel_word, set)
        self.push(stream)

    def push(self, stream):
        try:
            self.cs(0)
            time.sleep_ms(1)
            self.spi.write(stream)
        finally:
            self.cs(1)

    def channel_word(self, channel):
        if isinstance(channel, list):
            word = 0
            for i in channel:
                word += 2**i
        if isinstance(channel, int):
            word = 2**channel
        return word
