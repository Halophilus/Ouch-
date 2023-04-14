from gpiozero import LED, Button
from VideoPlayer import VLCVideoPlayer
from time import sleep
from pathlib import Path
import time

video_files = [("Startup", 5.080),
               ("Main Sequence 1",10.000), 
               ("Transition 1",2.000),
               ("Black Button", 3.000),
               ("Main Sequence 2",10.000),
               ("Transition 2",2.000),
               ("Yellow Button",3.000),
               ("Main Sequence 3",10.000),
               ("Transition 3", 2.000),
               ("Red Button", 3.000),
               ("Credits", 3.920),
               ("Shutdown Screen", 4.000),
               ("Shutdown", 5.000)
               ]
master_video = "/home/pi/Ouch-/master.mp4"

black_button = Button(8, pull_up=True, hold_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.2, hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.2, hold_repeat=True)

player = VLCVideoPlayer(video_files, master_video)

print(player)
time.sleep(100000)
monitor = LED(15)
power = LED(14)
monitor.on()
power.on()

player.play_section('Startup')

key_button.wait_for_press()

player.play_section('Main Sequence 1')

sleep(10)

player.play_section('Transition 1')

black_button.wait_for_press()

player.play_section('Black Button')

black_button.wait_for_release()

player.play_section('Main Sequence 2')

sleep(10)

player.play_section('Transition 2')

yellow_button.wait_for_press()

player.play_section('Yellow Button')

yellow_button.wait_for_release()

player.play_section('Main Sequence 3')

sleep(10)

player.play_section('Transition 3')

yellow_button.wait_for_press()

player.play_section('Red Button')

yellow_button.wait_for_release()

player.play_section('Credits')

sleep(3.920)

player.play_video('Shutdown Screen')

key_button.wait_for_release

player.stop()
monitor.off()
power.off()
