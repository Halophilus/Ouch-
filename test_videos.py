from gpiozero import LED, Button
from VideoPlayer import OmxplayerPlayer
from time import sleep

monitor = LED(15)
power = LED(14)
black_button = Button(8, pull_up=True, hold_time=0.2, hold_repeat=True)
yellow_button = Button(1, pull_up=True, hold_time=0.2, hold_repeat=True)
red_button = Button(7, pull_up=True, hold_time=0.2, hold_repeat=True)
key_button = Button(25, pull_up=True, hold_time=0.2, hold_repeat=True)

player = OmxplayerPlayer()

def timeRemaining():
    t = player.get_time_remaining
    sleep(t)

player.show_default_image()

monitor.on()

player.play("STARTUP_LOOP.MP4", loop=True)

key_button.wait_for_press()

player.play("Main Sequence/1.mp4")

timeRemaining()

player.play("Transitions/1.mp4", loop = True)

black_button.wait_for_press()

player.play("Button Press/BLACK.mp4", loop = True)

black_button.wait_for_release()

player.play("Main Sequence/2.mp4")

timeRemaining()

player.play("Transitions/2.mp4", loop = True)

yellow_button.wait_for_press()

player.play("Button Press/YELLOW.mp4", loop = True)

yellow_button.wait_for_release()

player.play("Main Sequence/3.mp4")

timeRemaining()

player.play("Transitions/3.mp4", loop = True)

yellow_button.wait_for_press()

player.play("Button Press/RED.mp4", loop = True)

yellow_button.wait_for_release()

player.play("CREDITS.MP4")
timeRemaining()
player.set_default_image("SHUTDOWN_FRAME.PNG")
key_button.wait_for_release
monitor.off()
power.off()
