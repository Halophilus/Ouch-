from gpiozero import LED, PWMLED, Button, RGBLED, PWMOutputDevice, DistanceSensor
import time

# LEDs
power = LED(14)
monitor = LED(15)
powerLight = RGBLED(18, 27, 22)
activity = LED(10)

# Fans
front_fan = PWMOutputDevice(12)
rear_fan = PWMOutputDevice(13)

# Buzzer
buzzer = PWMLED(6)

# Buttons
black_button = Button(8)
yellow_button = Button(1)
red_button = Button(7)
key_button = Button(25)

# Distance sensor
distance_sensor = DistanceSensor(echo=20, trigger=21)

# Test power LED
print("Testing power LED...")
power.on()
time.sleep(1)

# Test monitor LED
print("Testing monitor LED...")
monitor.on()
time.sleep(1)

# Test powerLight LED
print("Testing powerLight LED...")
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
for color in colors:
    powerLight.color = color
    print(f"PowerLight color: {color}")
    time.sleep(1)
powerLight.color = (1, 1, 1)

# Test activity LED
print("Testing activity LED...")
for _ in range(5):
    activity.toggle()
    time.sleep(1)
activity.on()

# Test fans
print("Testing front fan...")
for i in range(6):
    front_fan.value = i / 5
    time.sleep(1)
front_fan.off()

print("Testing rear fan...")
for i in range(6):
    rear_fan.value = i / 5
    time.sleep(1)
rear_fan.off()

# Test buzzer
print("Testing buzzer...")
for _ in range(3):
    buzzer.on()
    time.sleep(0.2)
    buzzer.off()
    time.sleep(0.2)

# Test buttons
def button_pressed(button_name):
    print(f"{button_name} button pressed")

def button_released(button_name):
    print(f"{button_name} button released")

buttons = [("black", black_button), ("yellow", yellow_button), ("red", red_button), ("key", key_button)]

for button_name, button in buttons:
    print(f"Press {button_name} button...")
    button.when_pressed = lambda: button_pressed(button_name)
    button.when_released = lambda: button_released(button_name)
    button.wait_for_release()
    time.sleep(0.5)

# Test distance sensor
print("Testing distance sensor...")
for i in range(1, 6):
    print(f"Move object to {i} feet away...")
    while distance_sensor.distance * 3.281 < i - 0.1 or distance_sensor.distance * 3.281 > i + 0.1:
        time.sleep(0.1)
    print(f"Object detected at {i} feet")

# Turn off everything
print("Turning off everything...")
power.off()
monitor.off()
powerLight.off()
activity.off()
front_fan.off()
rear_fan.off()
