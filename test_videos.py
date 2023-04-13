from gpiozero import LED, Button
from VideoPlayer import VLCVideoPlayer
from time import sleep
from pathlib import Path


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
monitor = LED(15)
power = LED(14)
black_button = Button(8, pull_up=True, hold_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.2, hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.2, hold_repeat=True)

player = VLCVideoPlayer(video_files, master_video)

monitor.on()
power.on()

player.play_video('Startup')

key_button.wait_for_press()

player.next_video()

sleep(15)

player.next_video()

black_button.wait_for_press()

player.next_video()

black_button.wait_for_release()

player.next_video()

sleep(15)

player.next_video()

yellow_button.wait_for_press()

player.next_video()

yellow_button.wait_for_release()

player.next_video()

sleep(15)

player.next_video()

yellow_button.wait_for_press()

player.next_video()

yellow_button.wait_for_release()

player.next_video()

sleep(15)

player.next_video()
key_button.wait_for_release
player.stop()
monitor.off()
power.off()
