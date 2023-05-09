#from gpiozero import LED, Button
from time import sleep
from pathlib import Path
import time
import looping_video
import gpiozero
import poll_result

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


# LEDs
power = gpiozero.LED(14)
monitor = gpiozero.LED(15)
powerLight = gpiozero.RGBLED(18, 27, 22)
activity = gpiozero.LED(10)

# Fans
front_fan = gpiozero.PWMOutputDevice(12)
rear_fan = gpiozero.PWMOutputDevice(13)

# Buttons with internal pull-up resistors and debounce-like behavior
black_button = gpiozero.Button(8, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
yellow_button = gpiozero.Button(1, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
red_button = gpiozero.Button(7, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)
key_button = gpiozero.Button(25, pull_up=True, hold_time=0.3, bounce_time=0.2, hold_repeat=True)

# Distance sensor
distance_sensor = gpiozero.DistanceSensor(echo=20, trigger=21)

# Buzzer
warning_buzzer = gpiozero.Buzzer(6)
button_panel = [black_button, yellow_button, red_button]


power.on()
class Script:
    def __init__(self):
        self._restart = False
        self._near = True

    def restart(self):
        player.skip_to_start(segment_name='initial_boot')
        player.loop_segment_later(segment_name='initial_boot')

    def wait_for_press(self, button):
        while True:
            if self._restart:
                return poll_result.PollResult.SHOULD_RESTART
            if button.is_pressed:
                return poll_result.PollResult.CONTINUE
            time.sleep(0.1)

    def wait_for_release(self, button):
        while True:
            if self._restart:
                return poll_result.PollResult.SHOULD_RESTART
            if not button.is_pressed:
                return poll_result.PollResult.CONTINUE
            time.sleep(0.1)

    def someone_is_near(self):
        self._near = True
        power.on()
        monitor.on()
        
    def no_one_near(self):
        self._near = False
        time.sleep(30)
        if not self._near:
            monitor.off()
            power.off()

    def _run(self):
        distance_sensor.when_in_range = lambda: self.someone_is_near()
        distance_sensor.when_out_of_range = lambda: self.no_one_near()
        # Set up buzzers
        def defaultButtonPress():
            warning_buzzer.on()
        def defaultButtonRelease():
            warning_buzzer.off()
        
        def rightButtonBuzzer():
            for _ in range(3):
                warning_buzzer.on()
                sleep(0.2)
                warning_buzzer.off()
                sleep(0.2)
        for button in button_panel:
            button.when_pressed = defaultButtonPress
            button.when_released = defaultButtonRelease

        monitor.on()

        print("WAITING FOR KEY BUTTON")
        if self.wait_for_press(key_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()

        player.skip_to_start(segment_name='sequence_1')
        player.loop_segment_later(segment_name='transition_1')

        print("WAITING FOR TRANSITION 3")
        player.wait_for_segment_to_be_reached(
            segment_name='transition_1',
            interrupt_check = lambda: self._restart
        )


        print("WAITING FOR BLACK BUTTON PRESS")
        black_button.when_pressed = rightButtonBuzzer
        if self.wait_for_press(black_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()

        player.skip_to_start(segment_name='button_1')
        player.loop_segment_later(segment_name='button_1')

        print("WAITING FOR BLACK BUTTON RELEASE")
        if self.wait_for_release(black_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()
        black_button.when_pressed = defaultButtonPress

        player.skip_to_start(segment_name='sequence_2')
        player.loop_segment_later(segment_name='transition_2')

        print("WAITING FOR TRANSITION 2")
        player.wait_for_segment_to_be_reached(
            segment_name='transition_2',
            interrupt_check = lambda: self._restart
        )

        print("WAITING FOR YELLOW BUTTON PRESS")
        yellow_button.when_pressed = rightButtonBuzzer
        if self.wait_for_press(yellow_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()

        player.skip_to_start(segment_name='button_2')
        player.loop_segment_later(segment_name='button_2')

        print("WAITING FOR YELLOW BUTTON RELEASE")
        if self.wait_for_release(yellow_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()
        yellow_button.when_pressed = defaultButtonPress
        
        player.skip_to_start(segment_name='sequence_3')
        player.loop_segment_later(segment_name='transition_3')

        print("WAITING FOR TRANSITION 3")
        player.wait_for_segment_to_be_reached(segment_name='transition_3')

        print("WAITING FOR RED BUTTON PRESS")
        red_button.when_pressed = rightButtonBuzzer
        if self.wait_for_press(red_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()
        player.skip_to_start(segment_name='button_3')
        player.loop_segment_later(segment_name='button_3')

        print("WAITING FOR RED BUTTON RELEASE")
        if self.wait_for_release(red_button) == poll_result.PollResult.SHOULD_RESTART:
            return self.restart()
        red_button.when_pressed = defaultButtonPress

        player.skip_to_start(segment_name='title_card')

        monitor.off()
        power.off()

    def run(self):
        while True:
            print("STARTING FROM THE TOP")
            self._run()
            print("RESTARTING")

if __name__ == '__main__':
    Script().run()