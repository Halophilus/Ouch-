
from gpiozero import LED, RGBLED, PWMOutputDevice
from colorzero import Color
from time import sleep
from VideoPlayer import OmxplayerPlayer
import looping_video
import random
import threading

master_video = './video.mp4_new_audio.mp4'

player = looping_video.LoopingVideo(filepath=master_video, segments={
        'initial_boot': looping_video.LoopingVideo.Segment(
            start=0,
            stop=40 # 40.791
        ),
        'sequence_1': looping_video.LoopingVideo.Segment(
            start=41, # 40.791
            stop="1:45" # 01:45:166
        ),
        'transition_1': looping_video.LoopingVideo.Segment(
            start="1:46", # 01:46:166
            stop="2:16" # 02:16:541
        ),
        'button_1': looping_video.LoopingVideo.Segment(
            start='2:17',# 02:16:541
            stop='2:40' # 02:40:291
        ),
        'sequence_2': looping_video.LoopingVideo.Segment(
            start='2:41',# 02:40:291
            stop='9:02' # 09:02:041
        ),
        'transition_2': looping_video.LoopingVideo.Segment(
            start='9:02', # 09:02:041
            stop='10:22' # 10:22:583
        ),
        'button_2': looping_video.LoopingVideo.Segment(
            start='10:23', # 10:22:583
            stop='10:43' # 10:43:458
        ),
        'sequence_3': looping_video.LoopingVideo.Segment(
            start='10:44', # 10:43:458
            stop='18:15' # 18:15:166
        ),
        'transition_3': looping_video.LoopingVideo.Segment(
            start='18:15', # 18:15:166
            stop='18:28' # 18:28:708
        ),
        'button_3': looping_video.LoopingVideo.Segment(
            start='18:29', # 18:28:708
            stop='18:55' # 18:55:708
        ),
        'title_card': looping_video.LoopingVideo.Segment(
            start='18:56', # 18:55:708
            stop='19:14' # 19:14:791
        ),
        'credits': looping_video.LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:50:625
        ),
        'shutdown_screen': looping_video.LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:55:958
        )
    })

function_thread = None
stop_thread = True

warning_buzzer = Buzzer(6)

power = LED(14)
monitor = LED(15)
activity = LED(10)
fog = LED(9)
powerLight = RGBLED(18,27,22, active_high = False)
powerLightColors = [(1,1,1),(0,0,0),(0,0,1),(0,1,1)]


black_button = Button(8, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
access_button = Button(25, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)

red_button_waiting = False
yellow_button_waiting = False
black_button_waiting = False

button_panel = [black_button, yellow_button, red_button]

def defaultButtonPress():
    warning_buzzer.on()
def defaultButtonRelease():
    warning_buzzer.off()
for button in button_panel:
    button.when_pressed = defaultButtonPress
    button.when_released = defaultButtonRelease

def wrongButtonBuzzer():
    for _ in range(3):
        warning_buzzer.on()
        sleep(0.2)
        warning_buzzer.off()
        sleep(0.2)
def red_button_press():
    global red_button_waiting
    if red_button_waiting:
        
    wrongButtonBuzzer()
def yellow_button_press():
    global yellow_button_waiting
    yellow_button_waiting = True
    wrongButtonBuzzer()
def black_button_press():
    global black_button_waiting
    black_button_waiting = True
    wrongButtonBuzzer()
        
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
fanSpeed = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

powerBoolean = False
sensor = DistanceSensor(echo=18, trigger=17, max_distance=4, threshold_distance=3.85)

def someone_is_near():
    global powerBoolean
    powerBoolean = True
    power.on()
    monitor.on()
def no_one_near():
    global powerBoolean
    powerBoolean = False
    sleep(30)
    if not powerBoolean:
        power.off()
        monitor.off()
sensor.when_in_range = someone_is_near
sensor.when_out_of_range = no_one_near

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
 


