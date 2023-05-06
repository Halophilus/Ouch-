from gpiozero import LED, PWMLED, Button, RGBLED, PWMOutputDevice, DistanceSensor
import time

def wait_for_input():
    input("Press ENTER to continue...")

def cleanup():
    print("Turning off all devices...")
    power.off()
    monitor.off()
    powerLight.off()
    activity.off()
    front_fan.off()
    rear_fan.off()
    buzzer.off()

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

# Buttons with internal pull-up resistors and debounce-like behavior
black_button = Button(8, pull_up=True, hold_time=0.3, bounce_time=0.2 hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.3, bounce_time=0.2 hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.3, bounce_time=0.2 hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.3, bounce_time=0.2 hold_repeat=True)


# Distance sensor
distance_sensor = DistanceSensor(echo=20, trigger=21)

try:
    # Test power LED
    print("Testing power LED...")
    power.on()
    wait_for_input()

    # Test monitor LED
    print("Testing monitor LED...")
    monitor.on()
    wait_for_input()

    # Test powerLight LED
    print("Testing powerLight LED...")
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    for color in colors:
        powerLight.color = color
        print(f"PowerLight color: {color}")
        time.sleep(1)
    powerLight.color = (1, 1, 1)
    wait_for_input()

    # Test activity LED
    print("Testing activity LED...")
    for _ in range(5):
        activity.toggle()
        time.sleep(1)
    activity.on()
    wait_for_input()

    # Test fans
    print("Testing front fan...")
    for i in range(6):
        front_fan.value = i / 5
        time.sleep(1)
    front_fan.off()
    wait_for_input()

    print("Testing rear fan...")
    for i in range(6):
        rear_fan.value = i / 5
        time.sleep(1)
    rear_fan.off()
    wait_for_input()

    # Test buzzer
    print("Testing buzzer...")
    for _ in range(3):
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        time.sleep(0.2)
    wait_for_input()

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
        wait_for_input()

    # Test distance sensor
    while True:
        distance_in_feet = distance_sensor.distance * 3.281
        print(f"Object detected at {distance_in_feet:.2f} feet")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Stopping script.")

finally:
    cleanup()
