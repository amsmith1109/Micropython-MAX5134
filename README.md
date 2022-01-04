# Micropython MAX5134
 Simple object definition in python for controlling the MAX5134. A 4-channel 16-bit digital to analog converter. Tested with an ESP8266.
 
 **Contents:**
- [pyisotopomer](#pyisotopomer)
  - [Features](#Features)
  - [Connections](#Connections)
  - [Use](#Use)

## Features
 - Write voltage to specified output pins (specify max voltage)
 - Pre-load voltage output with LDAC
 - Clear all DAC registers
 - Software shutdown of the DAC
 - Apply the DAC linearity function.

This module does not utilize the ALERT pin, nor does it have handling for daisy-chaining.

## Connections
From Wemos D1 Mini ESP8266 → MAX5134
 - D5 (GPIO14) → 10 (SCLK)
 - D7 (GPIO13) → 8 (DIN)
 - D8 (GPIO15) → 9 (CS)
 - Ground      → 7 & 15 (GND)
 - 5V          → 4 (DVDD)

It is highly recommended that you use a stable voltage regulator. The 5V rail typically drops to ~4V from USB power. If you insist on using the esp as the voltage reference, consider using the 3.3V rail:
 - 5V          → 2 (AVDD)
 - 3.3V        → 1 (REFI)

If using a REF02 → MAX5134
 - G           → 7 & 15 (GND)
 - 6 (Vout)    → 1 (REFI)
Connect REF02 pin 2 (Vin) to a >9V source.

Connect MAX5134 pins 13 (M/Z) and 12 (LDAC) to GND or DVDD depending on your application.

## Use
To initialize the object, define the CS and SPI pins, then attach it to the object. Below uses the pinout as described above for the wemos d1 mini with a 3.3V reference. It is not necessary to call the maximum voltage if you are using the ref02 as the default value is 5V:

from machine import Pin, SPI
from MAX5134 import MAX5134
spi = SPI(1, baudrate=400000)
cs = Pin(15, Pin.OUT)
vmax = 3.3
dac = MAX5134(cs, spi, vmax)

Commanding an output voltage is used with write command. The first argument specifies the output pin to set, and the second is the desired voltage. The pin selection can be a single pin 0 thru 3, or a list if you wish to set multiple pins at once. 

For a single pin:
```Python
dac.write(0, 2)  # Sets output pin 0 to 2 V
```

For all pins:
```Python
dac.write([0,1,2,3],1)  # Sets all pins to 1 V
```

To clear all dac registers:
```Python
dac.clear()
```

Placing a value on the LDAC register uses the same syntax as the write command. Unlike write, the value must later be pushed to the output:
```Python
dac.ldac(0, 2)  # Set the LDAC register to 2 V
```

Then load the LDAC register to the output of the specified pins:
```Python
dac.load(0) # Pushes LDAC register for pin 0 to the output
```

Software shutdown of a pin on the DAC:
```Python
dac.pwr(0)  # Turns off pin 0
```

Clear all registers and reset the DAC:
```Python
dac.clear()
```
