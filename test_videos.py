from gpiozero import LED, Button
from VideoPlayer import InteractiveVideoPlayer
from time import sleep
from pathlib import Path
from videoDuration import get_video_duration

video_files = ["/home/pi/Ouch-/STARTUP_LOOP.mp4",
               "/home/pi/Ouch-/Main Sequence/1.mp4",
               "/home/pi/Ouch-/Transitions/1.mp4",
               "/home/pi/Ouch-/Button Press/BLACK.mp4",
               "/home/pi/Ouch-/Main Sequence/2.mp4",
               "/home/pi/Ouch-/Transitions/2.mp4",
               "/home/pi/Ouch-/Button Press/YELLOW.mp4",
               "/home/pi/Ouch-/Main Sequence/3.mp4",
               "/home/pi/Ouch-/Transitions/3.mp4",
               "/home/pi/Ouch-/Button Press/RED.mp4",
               "/home/pi/Ouch-/CREDITS.mp4",
               "/home/pi/Ouch-/SHUTDOWN_SCREEN.MP4",
               "/home/pi/Ouch-/SHUTDOWN.MP4"
               ]

monitor = LED(15)
power = LED(14)
black_button = Button(8, pull_up=True, hold_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.2, hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.2, hold_repeat=True)

player = InteractiveVideoPlayer(video_files)

def sleepForVideoDuration():
    current_video_path = player.video_files[player.current_video_index]
    time = get_video_duration(current_video_path)
    sleep(time)

monitor.on()
power.on()
player.reset
player.play_video(video_files[0])

key_button.wait_for_press()

player.next_video()

sleepForVideoDuration()

player.next_video()

black_button.wait_for_press()

player.next_video()

black_button.wait_for_release()

player.next_video()

sleepForVideoDuration()

player.next_video()

yellow_button.wait_for_press()

player.next_video()

yellow_button.wait_for_release()

player.next_video()

sleepForVideoDuration()

player.next_video()

yellow_button.wait_for_press()

player.next_video()

yellow_button.wait_for_release()

player.next_video()

sleepForVideoDuration()

player.next_video()
key_button.wait_for_release
player.stop()
monitor.off()
power.off()
