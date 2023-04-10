from gpiozero import LED, Button
from VideoPlayer import VideoEngine
from time import sleep
from pathlib import Path


monitor = LED(15)
power = LED(14)
black_button = Button(8, pull_up=True, hold_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.2, hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.2, hold_repeat=True)

player = VideoEngine()

monitor.on()
power.on()
player.play_video(Path("/home/pi/Ouch-/STARTUP_LOOP.mp4"), loop=True)

key_button.wait_for_press()

player.replace_video("/home/pi/Ouch-/Main Sequence/1.mp4")

t = player.get_time_remaining()
sleep(t)

player.replace_video("/home/pi/Ouch-/Transitions/1.mp4", loop = True)

black_button.wait_for_press()

player.replace_video("/home/pi/Ouch-/Button Press/BLACK.mp4", loop = True)

black_button.wait_for_release()

player.replace_video("/home/pi/Ouch-/Main Sequence/2.mp4")

t = player.get_time_remaining()
sleep(t)

player.replace_video("/home/pi/Ouch-/Transitions/2.mp4", loop = True)

yellow_button.wait_for_press()

player.replace_video("/home/pi/Ouch-/Button Press/YELLOW.mp4", loop = True)

yellow_button.wait_for_release()

player.replace_video("/home/pi/Ouch-/Main Sequence/3.mp4")

t = player.get_time_remaining()
sleep(t)

player.replace_video("/home/pi/Ouch-/Transitions/3.mp4", loop = True)

yellow_button.wait_for_press()

player.replace_video("/home/pi/Ouch-/Button Press/RED.mp4", loop = True)

yellow_button.wait_for_release()

player.replace_video("/home/pi/Ouch-/CREDITS.mp4")

t = player.get_time_remaining()
sleep(t)

player.display_image("/home/pi/Ouch-/SHUTDOWN_FRAME.png")
key_button.wait_for_release
player.stop()
monitor.off()
power.off()
