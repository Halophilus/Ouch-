from time import sleep
<<<<<<< HEAD
from pathlib import Path
import time
import random
import threading
import looping_video
from gpiozero import Button, Buzzer, LED, RGBLED, PWMOutputDevice
=======
from VideoPlayer import OmxplayerPlayer
import looping_video
import random
import threading
>>>>>>> parent of 16854447 (Add peripheral files)

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
<<<<<<< HEAD
            stop='19:15' # 19:14:791
=======
            stop='19:14' # 19:14:791
>>>>>>> parent of 16854447 (Add peripheral files)
        ),
        'credits': looping_video.LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:50:625
        ),
        'shutdown_screen': looping_video.LoopingVideo.Segment(
<<<<<<< HEAD
            start='20:51', # 19:14:791
            stop='20:56' # 20:55:958
        ),
        'shutdown_loop': looping_video.LoopingVideo.Segment(
            start= '20:56',
            stop='20:58'
        )
    })

player.start(initial_segment_name='initial_boot')


class FlickeringLight:
    def __init__(self, *, led, freq=2):
        self._led = led
        self._kill = False
        self._freq = freq
        self._thread = None

    def _activity(self):
        try:
            while True:
                print("L", flush=True)
                if self._kill:
                    self._thread = None
                    break
                time.sleep(random.uniform(0,self._freq))
                self._led.on()
                time.sleep(random.uniform(0, self._freq/2))
                self._led.off()
        except Exception as e:
            print(e, flush=True)
            self._activity()

    def start(self):
        if self._thread is not None:
            raise Exception("Already started")

        self._thread = threading.Thread(
            target = self._activity, 
            daemon = True
        )
        self._thread.start()
    
    def stop(self):
        self._kill = True

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, new_freq):
        self._freq = new_freq

led = LED(10)
led.off()
activity = FlickeringLight(
    led=led
)
=======
            start='19:14', # 19:14:791
            stop='20:50' # 20:55:958
        )
    })

function_thread = None
stop_thread = True
>>>>>>> parent of 16854447 (Add peripheral files)

warning_buzzer = Buzzer(6)
fog = LED(9)

black_button = Button(8, pull_up=True, hold_time=0.3, bounce_time=0.2)
yellow_button = Button(1, pull_up=True, hold_time=0.3, bounce_time=0.2)
red_button = Button(7, pull_up=True, hold_time=0.3, bounce_time=0.2)
access_button = Button(25, pull_up=True, hold_time=0.3, bounce_time=0.2)

button_panel = [black_button, yellow_button, red_button]

def defaultButtonPress():
    warning_buzzer.on()
def defaultButtonRelease():
    warning_buzzer.off()
for button in button_panel:
    button.when_pressed = defaultButtonPress
    button.when_released = defaultButtonRelease

monitor = LED(15)
power = LED(14)
powerLight = RGBLED(18, 27, 22)
frontFan = PWMOutputDevice(12)
rearFan = PWMOutputDevice(13)

monitor.on()
power.on()

print("WAITING FOR KEY BUTTON")
access_button.wait_for_press()
player.skip_to_start(segment_name='sequence_1')
frontFan.value = 0.4
rearFan.value = 0.4
print("FLICKERING")
activity.start()
player.loop_segment_later(segment_name='transition_1')

print("WAITING FOR TRANSITION 1")
player.wait_for_segment_to_be_reached(segment_name='transition_1')


print("WAITING FOR BLACK BUTTON PRESS")
black_button.wait_for_press()
player.skip_to_start(segment_name='button_1')
player.loop_segment_later(segment_name='button_1')
powerLight.color = (0,0,1)

print("WAITING FOR BLACK BUTTON RELEASE")
black_button.wait_for_release()
sleep(3)
for _ in 3:
    warning_buzzer.on()
    sleep(0.2)
    warning_buzzer.off()
    sleep(0.2)
frontFan = 0.6
rearFan = 0.6
activity.freq = 0.5
player.skip_to_start(segment_name='sequence_2')
player.loop_segment_later(segment_name='transition_2')

print("WAITING FOR TRANSITION 2")
player.wait_for_segment_to_be_reached(segment_name='transition_2')

print("WAITING FOR YELLOW BUTTON PRESS")
yellow_button.wait_for_press()
player.skip_to_start(segment_name='button_2')
powerLight.color = (0,1,1)
player.loop_segment_later(segment_name='button_2')

print("WAITING FOR YELLOW BUTTON RELEASE")
yellow_button.wait_for_release()
sleep(3)
for _ in 3:
    warning_buzzer.on()
    sleep(0.2)
    warning_buzzer.off()
    sleep(0.2)
rearFan.value = 0.8
frontFan.value = 0.8
activity.freq = 0.25
player.skip_to_start(segment_name='sequence_3')
player.loop_segment_later(segment_name='transition_3')

print("WAITING FOR TRANSITION 3")
player.wait_for_segment_to_be_reached(segment_name='transition_3')

print("WAITING FOR RED BUTTON PRESS")
red_button.wait_for_press()
powerLight.color = [0,1,0]
player.skip_to_start(segment_name='button_3')
player.loop_segment_later(segment_name='button_3')

print("WAITING FOR RED BUTTON RELEASE")
red_button.wait_for_release()
sleep(3)
for _ in 3:
    warning_buzzer.on()
    sleep(0.2)
    warning_buzzer.off()
    sleep(0.2)
frontFan.value = 1.0
rearFan.value = 1.0
player.skip_to_start(segment_name='title_card')
player.loop_segment_later(segment_name='title_card')
player.wait_for_segment_to_be_reached(segment_name='credits')
activity.freq = 0.1
monitor.off()


sleep(3)
sleep(1)
frontFan.value = 0.2
rearFan.value = 0.2
sleep(3)
power.off()
activity.stop()
frontFan.value = 0.0
rearFan.value = 0.0
powerLight.color = (1,1,1)
sleep(5)
player.skip_to_start(segment_name='credits')
player.loop_segment_later(segment_name='shutdown_screen')
power.on()
monitor.on()
print("WAITING FOR KEY RELEASE")
access_button.wait_for_release()
player.skip_to_start(segment_name='shutdown_loop')
sleep(3)
power.off()
monitor.off()


