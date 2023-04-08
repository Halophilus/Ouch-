
from gpiozero import LED, RGBLED, PWMOutputDevice
from colorzero import Color
from time import sleep
from VideoPlayer import OmxplayerPlayer
import random
import threading

player = OmxplayerPlayer()
function_thread = None
stop_thread = True

warning_buzzer = Buzzer(6)

power = LED(14)
monitor = LED(15)
activity = LED(10)
fog = LED(9)
powerLight = RGBLED(18,27,22, active_high = False)

access_button = Button(25)
red_button = Button(7)
yellow_button = Button(1)
black_button = Button(8)

def defaultButtonPress():
    warning_buzzer.on()

def defaultButtonRelease():
    warning_buzzer.off()

red_button.when_pressed = defaultButtonPress
yellow_button.when_pressed = defaultButtonPress
black_button.when_pressed = defaultButtonPress

red_button.when_released = defaultButtonRelease
yellow_button.when_released = defaultButtonRelease
black_button.when_released = defaultButtonRelease

red_button_waiting = False
yellow_button_waiting = False
black_button_waiting = False

def red_button_press():
    global red_button_waiting
    red_button_waiting = True
    for _ in range(3):
        warning_buzzer.on()
        sleep(0.2)
        warning_buzzer.off()
def yellow_button_press():
    global yellow_button_waiting
    yellow_button_waiting = True
    for _ in range(3):
        warning_buzzer.on()
        sleep(0.2)
        warning_buzzer.off()
def black_button_press():
    global black_button_waiting
    black_button_waiting = True
    for _ in range(3):
        warning_buzzer.on()
        sleep(0.2)
        warning_buzzer.off()

def red_button_release():
    global red_button_waiting
    red_button_waiting = False
    red_button.when_released = defaultButtonRelease
    red_button.when_pressed = defaultButtonPress
def yellow_button_release():
    global yellow_button_waiting
    yellow_button_waiting = False
    yellow_button.when_released = defaultButtonRelease
    yellow_button.when_pressed = defaultButtonPress
def black_button_release():
    global black_button_waiting
    black_button_waiting = False
    black_button.when_released = defaultButtonRelease
    black_button.when_pressed = defaultButtonPress

frontFan = PWMOutputDevice(12)
rearFan = PWMOutputDevice(13)

lowFanHz = 0.2
lowPlusHz = 0.4
midFanHz = 0.6
hiFanHz = 0.8

sensor = DistanceSensor(echo=18, trigger=17)


flickerFreq = 2
flickill = False
def flickerActivity():
    while True:
        if flickill:
            break
        sleep(random.uniform(0,flickerFreq))
        activity.on()
        sleep(random.uniform(0, flickerFreq/2))
        activity.off()
flickerThread =  threading.Thread(target = flickerActivity, daemon = True)

def button_pressed():
    # Run the function in a separate thread
    global stop_thread, function_thread
    stop_thread = False
    function_thread = threading.Thread(target=run_sequence, daemon = True)
    function_thread.start()


def run_sequence():
    global stop_thread
    global black_button_waiting
    global yellow_button_waiting
    global red_button_waiting
    global flickerFreq, flickill
    while not stop_thread:
        button_tracker = False
        player.play("Main Sequence/1.MP4")
        powerLight.color(0,1,1)
        activity.off()
        flickerThread.start()
        flickerFreq = 0.5
        rearFan.value = lowPlusHz
        frontFan.value = lowPlusHz
        t = player.get_time_remaining()
        if stop_thread:
            break
        for _ in range(t):
            sleep(1)
            if stop_thread:
                break
        if stop_thread:
            break
        player.play("Transitions/1.MP4", loop = True)
        while not black_button_waiting:
            if not button_tracker:
                black_button.when_pressed = black_button_press
                black_button.when_released = black_button_release
                button_tracker = True
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        player.play("Button Press/BLACK.MP4", loop = True)
        while black_button_waiting:
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        player.play("Main Sequence/2.MP4")
        powerLight.color(1,0,1)
        flickerFreq = 0.25
        rearFan.value = midFanHz
        frontFan.value = midFanHz
        t = player.get_time_remaining()
        for _ in range(t):
            if stop_thread:
                break
            sleep(1)
        if stop_thread:
            break
        player.play("Transitions/2.MP4", loop=True)
        while not yellow_button_waiting:
            if button_tracker:
                yellow_button.when_pressed = yellow_button_press
                yellow_button.when_released = yellow_button_release
                button_tracker = False
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        player.play("Button Press/YELLOW.MP4", loop=True)
        while yellow_button_waiting:
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        player.play("Main Sequence/3.MP4")
        powerLight.color(1,1,0)
        flickerFreq = 0.1
        rearFan.value = hiFanHz
        frontFan.value = hiFanHz
        t = player.get_time_remaining()
        for _ in range(t):
            if stop_thread:
                break
            sleep(1)
        if stop_thread:
            break
        player.play("Transitions/3.MP4", loop=True)
        while not red_button_waiting:
            if not button_tracker:
                red_button.when_pressed = red_button_press
                red_button.when_released = red_button_release
                button_tracker = True
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        player.play("Button Press/RED.MP4", loop=True)
        while red_button_waiting:
            if stop_thread:
                break
            sleep(0.1)
        if stop_thread:
            break
        rearFan.value = 1.0
        frontFan.value = 1.0
        sleep(random.uniform(0,3))
        monitor.off()
        sleep(random.uniform(0,3))
        fog.on()
        if stop_thread:
            break        
        sleep(1)
        powerLight.off()
        flickill = True
        if stop_thread:
            break  
        sleep(0.75)
        sleep(1)
        fog.off()
        rearFan.value = 0.2
        frontFan.value = 0.2
        for i in range(15):
            if stop_thread:
                break
            sleep(1)
        if stop_thread:
            break
        rearFan.value = 0
        frontFan.value = 0
        player.show_default_image()
        monitor.on()
        activity.blink(on_time = 1, off_time = 1)
        powerLight.pulse(on_color = (0,1,0.5),off_color = (1,0.5,0))
        player.play("CREDITS.MP4")
        t = player.get_time_remaining()
        for _ in range(t):
            if stop_thread:
                break
            sleep(1)
        if stop_thread:
            break
        player.set_default_image("SHUTDOWN_FRAME.PNG")
        access_button.wait_for_release()
        sleep(0.1)


def when_released():
    global stop_thread, function_thread
    stop_thread = True
    red_button.when_pressed = defaultButtonPress
    yellow_button.when_pressed = defaultButtonPress
    black_button.when_pressed = defaultButtonPress

    red_button.when_released = defaultButtonRelease
    yellow_button.when_released = defaultButtonRelease
    black_button.when_released = defaultButtonRelease
    
    access_button.when_held = None
    access_button.when_released = None

    red_button_waiting = False
    yellow_button_waiting = False
    black_button_waiting = False



i = 0  
while True:
    player.set_default_image("BLANK.JPG")
    distance = sensor.distance
    while distance >= 150:
        if i == 0:
            player.play("STARTUP_LOOP.MP4", loop = True)
            access_button.when_held = button_pressed
            access_button.when_released = when_released
            rearFan.value = lowFanHz
            power.on()
            monitor.on()
            activity.blink(on_time = 1, off_time = 1)
            powerLight.on()
            i = 1
        for _ in range(30):
            while access_button.is_held:
                sleep(1)
            if stop_thread:
                break
            sleep(1)
        if stop_thread:
            break
        sleep(0.1)
    fog.off()
    player.play("SHUTDOWN.MP4")
    t = player.get_time_remaining()
    sleep(t)
    player.show_default_image()
    sleep(random.uniform(0,2))
    monitor.off()
    player.off()
    sleep(random.uniform(0,1))
    rearFan.value = 0
    frontFan.value = 0
    sleep(random.uniform(0,0.75))
    powerLight.off()
    power.off()
    i = 0

    sleep(30)
 


