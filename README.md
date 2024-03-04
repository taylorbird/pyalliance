# pytelink

A python library to perform basic control functionality for telink-based BLE lights. Uses `python-dimond` for the low-level
communications, and implements a helpful library on top that has light-specific features.

## Library Usage

```
from pytelink import Controller
controller = Controller("FF:00:00:00:00:00", "MeshName", "MeshPassword")
controller.start()

# ... a few seconds later ...

controller.lights() # returns a dict[address, Light]
light = controller.light(5) # get a light
light.is_on() # returns boolean
light.turn_off()
light.turn_on()
light.set_brightness(50)
light.set_color(255, 0, 255)
light.set_temperature(200)

# or all lights at once
controller.all().turn_off()
controller.all().turn_on()
# ... and so on

```

## Mesh info
You can use `bluetoothctl` to find the Mac address of a light to use as your entry into the mesh (the first param to Controller()). The Mesh Name is whatever shows up in your lights' native app, and the Mesh Password is very likely hard-coded to the literal `2846` regardless of what the native app says.