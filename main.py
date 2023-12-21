from time import sleep
from pathlib import Path
import time, random, threading, looping_video
from flickering_light import FlickeringLight
from gpiozero import Button, Buzzer, LED, RGBLED, PWMOutputDevice, DistanceSensor

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
            stop='19:15' # 19:14:791
        ),
        'credits': looping_video.LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:50:625
        ),
        'shutdown_screen': looping_video.LoopingVideo.Segment(
            start='20:51', # 19:14:791
            stop='20:56' # 20:55:958
        ),
        'shutdown_loop': looping_video.LoopingVideo.Segment(
            start= '20:56',
            stop='20:58'
        )
    })

led = LED(10)
led.off()
activity = FlickeringLight(
    led=led
)

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

sequence_start = False
def key_button_press():
    global sequence_start
    sequence_start = True
def key_button_release():
    global sequence_start
    sequence_start = False


monitor = LED(15)
power = LED(14)
powerLight = RGBLED(18, 27, 22)
frontFan = PWMOutputDevice(12)
rearFan = PWMOutputDevice(13)

# Proximity sensor for enabling/disabling the monitor
distance_sensor = DistanceSensor(echo=20, trigger=21)
def in_range_function():
    global in_range
    in_range = True
def out_of_range_function():
    global in_range
    in_range = False

loop_completed = False

def main():
    while True:
        '''
            Main video loop sequence notes:
                As much of this script as possible is written consecutively within one code block to avoid race conditions due to concurrent calls on the same objects. 
                This posed its own issues under initial deployment.
                All functions related to the state of gpiozero objects control global variables that manipulate the control structure of the main loop.
                This overall structure was originally meant to be more responsive to new key turns and walking away from the sensor, but these posed unique race conditions that distracted from the main presentation
                The code for the fog machine is presently omitted so that this can be run in public buildings / schools, but it can be added easily, treating the gate pin as an LED. 
        '''
        if loop_completed: # If this is the second pass through the loop
            player.skip_to_start(initial_segment_name='initial_boot') # Track back to initial sequence
            sequence_start = False # This is performed redundantly to accommodate for gpiozero glitching
        else:
            player.start(initial_segment_name='initial_boot')
        while not sequence_start: # If the key has not been turned
            monitor.off()
            power.off()
            while in_range:
                if sequence_start():
                    break
                monitor.on()
                power.on()
                sleep(1) # More time alotted to account for artifacts in sensor reading
            sleep(0.1) # Adds responsiveness to new motion

        '''
            GENERAL STRUCTURE:
                1. Skip to start of sequence
                2. Set fan speeds
                3. Start activity light
                4. Wait for transition sequence.
                5. Loop corresponding transition sequence after the first sequence completes
                6. Wait for button press
                7. Start looping button press sequence
                8. Change powerLight LED color
                    - This is skipped for the first act because common cathode LEDs are on by default
                9. Wait for button release
                10. Beep the piezoelectric buzzer three times
                11. Return to step 1 for the following sequence
        '''
        ## SEQUENCE 1 ##

        # Skip to the start of the sequence
        player.skip_to_start(segment_name='sequence_1')
        
        # 40% fan duty cycle
        frontFan.value = 0.4
        rearFan.value = 0.4
        
        # Initiate flickering thread
        print("FLICKERING")
        activity.start()
        
        # Set up transition loop while the first sequence is playing
        player.loop_segment_later(segment_name='transition_1')
        print("WAITING FOR TRANSITION 1")
        player.wait_for_segment_to_be_reached(segment_name='transition_1')

        # Wait for button press to change states
        print("WAITING FOR BLACK BUTTON PRESS")
        black_button.wait_for_press()

        # Set up button press sequence loop
        player.skip_to_start(segment_name='button_1')
        player.loop_segment_later(segment_name='button_1')
        
        # Change powerLight LED color
        powerLight.color = (0,0,1)

        # Button release protocol
        print("WAITING FOR BLACK BUTTON RELEASE")
        black_button.wait_for_release()
        sleep(3) # Let viewer get a good look at the button press sequence
        for _ in 3: # Handled within main loop to avoid changing when_pressed functions / race conditions
            warning_buzzer.on() # Beep three times
            sleep(0.2)
            warning_buzzer.off()
            sleep(0.2)

        ## SEQUENCE 2 ##
        
        player.skip_to_start(segment_name='sequence_2')

        frontFan.value = 0.6
        rearFan.value = 0.6

        # Alter the flicker frequency for the existing flickering thread
        activity.freq = 0.5

        player.loop_segment_later(segment_name='transition_2')
        print("WAITING FOR TRANSITION 2")
        player.wait_for_segment_to_be_reached(segment_name='transition_2')

        print("WAITING FOR YELLOW BUTTON PRESS")
        yellow_button.wait_for_press()
        player.skip_to_start(segment_name='button_2')
        player.loop_segment_later(segment_name='button_2')

        powerLight.color = (0,1,1)
        
        print("WAITING FOR YELLOW BUTTON RELEASE")
        yellow_button.wait_for_release()
        sleep(3)
        for _ in 3:
            warning_buzzer.on()
            sleep(0.2)
            warning_buzzer.off()
            sleep(0.2)
        
        ## SEQUENCE 3 ##

        player.skip_to_start(segment_name='sequence_3')

        rearFan.value = 0.8
        frontFan.value = 0.8

        activity.freq = 0.25

        player.loop_segment_later(segment_name='transition_3')
        print("WAITING FOR TRANSITION 3")
        player.wait_for_segment_to_be_reached(segment_name='transition_3')

        print("WAITING FOR RED BUTTON PRESS")
        red_button.wait_for_press()
        
        player.skip_to_start(segment_name='button_3')
        player.loop_segment_later(segment_name='button_3')

        powerLight.color = (0,1,0)

        print("WAITING FOR RED BUTTON RELEASE")
        red_button.wait_for_release()
        sleep(3)
        for _ in 3:
            warning_buzzer.on()
            sleep(0.2)
            warning_buzzer.off()
            sleep(0.2)
        
        ## FINAL BUTTON PRESS SEQUENCE ##
        
        frontFan.value = 1.0
        rearFan.value = 1.0

        player.skip_to_start(segment_name='title_card')
        player.loop_segment_later(segment_name='title_card')
        player.wait_for_segment_to_be_reached(segment_name='credits')
        
        activity.freq = 0.1
        
        monitor.off() # Screen shuts off first

        sleep(4) # Computer runs briefly before totally losing power

        frontFan.value = 0.2
        rearFan.value = 0.2
        sleep(3)
        power.off() # Disengages most peripherals by cutting power
        
        activity.freq = 1.0 # Returns to default freq value
        activity.stop() # Closes flickering thread

        frontFan.value = 0.0 # Disengages both fans
        rearFan.value = 0.0

        powerLight.color = (1,1,1) # Sets power LED to off (common cathode, highs indicate off position)

        sleep(5) # Create suspense

        ## CREDITS SEQUENCE ##

        player.skip_to_start(segment_name='credits')
        player.loop_segment_later(segment_name='shutdown_screen') # Final screen prompting key release
        
        power.on() # Power comes back on minus auditory peripherals
        monitor.on()
        
        # This section checks to see if the key has been released through the sequence start variable, as gpiozero has been glitchy with this many peripherals
        player.wait_for_segment_to_be_reached(segment_name='shutdown_screen')
        print("WAITING FOR KEY RELEASE")
        while sequence_start:
            sleep(0.1)

        ## SHUTDOWN SEQUENCE ##
        player.skip_to_start(segment_name='shutdown_loop')
        sleep(3)
        power.off()
        monitor.off()

if __name__ == '__main__':
    main()
