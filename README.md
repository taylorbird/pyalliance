# pytelink

A python library to perform basic control functionality for telink-based BLE lights. Uses `python-dimond` for the low-level
communications, and implements a helpful library on top that has light-specific features.

## Library Usage

```
from pytelink import Controller
controller = Controller()
controller.start()

# ... a few seconds later ...

controller.lights() # returns a dict[address, Light]
light = controller.lights()[5] # get a light
light.is_on() # returns boolean
light.turn_off()
light.turn_on()
light.set_brightness(50)
light.set_color(255, 0, 255)
light.set_temperature(200)
```

