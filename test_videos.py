#from gpiozero import LED, Button
from time import sleep
from pathlib import Path
import time
import looping_video
import gpiozero


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

player.start(initial_segment_name='initial_boot')
black_button = gpiozero.Button(8, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
yellow_button = gpiozero.Button(1, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
red_button = gpiozero.Button(7, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
# There is a typo in the code. It should be `red_button = gpiozero.Button(7, pull_up=True,
# hold_time=0.2, hold_repeat=True)`. This line of code is creating a Button object for a physical
# button connected to GPIO pin 7 on the Raspberry Pi. The `pull_up=True` argument enables the internal
# pull-up resistor on the pin, and the `hold_time` and `hold_repeat` arguments specify the duration
# and repetition of the button hold event.
key_button = gpiozero.Button(25, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)

monitor = gpiozero.LED(15)
power = gpiozero.LED(14)
monitor.on()
power.on()

print("WAITING FOR KEY BUTTON")
key_button.wait_for_press()
player.skip_to_start(segment_name='sequence_1')
player.loop_segment_later(segment_name='transition_1')

print("WAITING FOR TRANSITION 3")
player.wait_for_segment_to_be_reached(segment_name='transition_1')


print("WAITING FOR BLACK BUTTON PRESS")
black_button.wait_for_press()
player.skip_to_start(segment_name='button_1')
player.loop_segment_later(segment_name='button_1')

print("WAITING FOR BLACK BUTTON RELEASE")
black_button.wait_for_release()
player.skip_to_start(segment_name='sequence_2')
player.loop_segment_later(segment_name='transition_2')

print("WAITING FOR TRANSITION 2")
player.wait_for_segment_to_be_reached(segment_name='transition_2')

print("WAITING FOR YELLOW BUTTON PRESS")
yellow_button.wait_for_press()
player.skip_to_start(segment_name='button_2')
player.loop_segment_later(segment_name='button_2')

print("WAITING FOR YELLOW BUTTON RELEASE")
yellow_button.wait_for_release()
player.skip_to_start(segment_name='sequence_3')
player.loop_segment_later(segment_name='transition_3')

print("WAITING FOR TRANSITION 3")
player.wait_for_segment_to_be_reached(segment_name='transition_3')

print("WAITING FOR RED BUTTON PRESS")
red_button.wait_for_press()
player.skip_to_start(segment_name='button_3')
player.loop_segment_later(segment_name='button_3')

print("WAITING FOR RED BUTTON RELEASE")
red_button.wait_for_release()

player.skip_to_start(segment_name='title_card')

monitor.off()
power.off()

