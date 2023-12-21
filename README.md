# OUCH! Project - Software Documentation

## Introduction
![Project Overview](/Documentation/images/title.png)
This is an overview of the software section of this project. To see the hardware specifications, visit the [Hardware Summary Page](/Documentation/hardware_summary.md)

## Table of Contents
1. [Introduction](#introduction)
2. [Main Script - main.py](#main-script---mainpy)
3. [Looping Video Class - looping_videos.py](#looping-video-class---looping_videospy)
4. [How to Run](#how-to-run)
5. [Ouch! Drama](#ouch-drama)
6. [Dependencies](#dependencies)
7. [Image gallery](#image-gallery)
8. [License](#license)
9. [Contact](#contact)
10. [Acknowledgments](#acknowledgments)

## Introduction
This README provides documentation for the scripts used in the OUCH! hardware project. The scripts control various hardware components, including video playback, LED control, and sensor interactions.

## Main Script - main.py
The main.py script serves as the central controller for an interactive hardware-based project. It primarily handles video playback management using predefined segments and controls various hardware components like LEDs, fans, and buttons through the Raspberry Pi's GPIO pins.

### Script Components and Functionalities

1. **Import Statements**
    - The script begins by importing necessary Python modules like time, pathlib.Path, random, threading, and gpiozero.
    - looping_video is a custom module used for handling video playback.

2. **Video Playback Setup**
    - master_video variable holds the path to the main video file.
    - An instance of looping_video.LoopingVideo is created, which manages the playback of different segments of the video.
    - Each segment is defined with start and stop times, allowing for precise control over which part of the video is played.

4. **FlickeringLight Class**
    - This custom class manages a flickering LED effect. 
    - It uses threading to control the on and off timing of an LED to create a flickering appearance.
    - The class provides methods to start and stop the flickering effect and allows frequency adjustment for the flickering.

5. **GPIO Component Initialization**
    - The script initializes various GPIO components using the gpiozero library:
        - LED and RGBLED objects for controlling LEDs.
        - Button objects for handling physical button presses.
        - Buzzer for audio feedback.
        - PWMOutputDevice for controlling fan speeds.

6. **Power and Monitor Control**
    - LEDs representing the power and monitor are switched on using .on() method, indicating that the system is active.

7. **Button Interaction Setup**
    - The script sets up listeners for button press events. Each button is linked to a function that defines what action should be taken when the button is pressed or released.
    - The use of hold_time and bounce_time parameters helps in debouncing the buttons and avoiding false triggers.

8. **Video Segment Control**
    - The script waits for specific events (like a button press) to progress through different segments of the video.
    - For each segment, it controls which part of the video should be played and loops certain sections.

9. **Fan Speed Control**
    - Using PWMOutputDevice, the script controls the speed of fans connected to the GPIO.
    - This can be used to manage fan sounds based on the state of the sequence to contribute to the project's interactive elements.

10. **Shutdown Sequence**
    - The script includes a shutdown sequence where it turns off various components and moves the video to a shutdown screen.

---

### Looping Videos Script - looping_videos.py

1. **LoopingVideo Class**
    - Manages video playback using the python_mpv_jsonipc library, which provides an interface to the MPV media player.
    - Allows defining segments of a video with precise start and stop times.
    Can loop specific segments and wait for certain segments to reach their end.

2. **Class Methods**
    - start: Initiates video playback with a specified segment.
    - skip_to_start: Skips to the start of a specific segment.
    - loop_segment_later: Sets a segment to loop after it starts.
    - wait_for_segment_to_be_reached: Pauses script execution until a specified segment is reached.

---

### Script Execution Flow

The script combines these functionalities to create an interactive experience. For example, it might start with an introductory video segment, wait for a user to press a button, and then move to the next segment, all the while controlling lights and fans to enhance the interaction.

This script demonstrates a complex interaction of hardware control and video playback management, suitable for interactive installations or multimedia projects. The use of GPIO with the Raspberry Pi and the integration of video segments with physical interactions provides a rich and engaging user experience.

### Key Components
- `looping_video.LoopingVideo`: A class imported from `looping_videos.py` for handling video playback.
- `gpiozero` components: For interfacing with GPIO pins on the Raspberry Pi.
- `FlickeringLight`: A custom class for creating a flickering LED effect.

## Looping Video Class - looping_videos.py
The `looping_videos.py` script contains the `LoopingVideo` class, which manages video playback on loop with defined segments. This class is used in `main.py` to control the video flow of the project.

### Features
- Segment-based video playback.
- Synchronization of video segments with hardware actions.
- Flexible control over video start and stop times.

## How to Run
To run these scripts on your Raspberry Pi:
1. Ensure all hardware is properly connected.
2. Install required dependencies (see below).
3. Execute `main.py` to start the program: `python main.py`

## OUCH! drama

1. The program utilizes a distance sensor to detect when a person is within 150 cm.
2. When a person is within range, the program starts looping the startup sequence and the screen turns on.
3. The first sequence starts only when the access key is turned on.
4. The program plays the first act of the film, then starts playing the transition sequence.
5. The transition sequence loops until the black button ('SELECT') is pressed.
6. If the right button is pressed during a transition sequence, the piezoelectric buzzer beeps three times and the button press sequence starts playing.
7. As long as the button is held, the button press sequence loops.
8. Once released, the next act in the film plays.
9. If a button is pressed and held outside of the relevant sequences, it will play a continuous beeping sound.
10. At the end of the second act, the second transition sequence starts looping until the yellow button ('A-35') is pressed.
11. The final act of the film plays, reaches transition, then prompts for the final button press (red, 'the right decision').
12. At the end of the final button press sequence, the screen briefly shuts off and all GPIO devices are deactivated briefly.
13. The screen turns back on and the credits sequence begins.
14. At the end of the credits sequence, dismount is prompted.
15. When the viewer turns the key off, the shutdown sequence plays and the device resets. 

## Dependencies
- Python 3.x
- [python_mpv_jsonipc](https://pypi.org/project/python-mpv-jsonipc/): For handling MPV player.
- [gpiozero](https://gpiozero.readthedocs.io/): For Raspberry Pi GPIO interactions.

Install dependencies using pip:
```bash
pip install python-mpv-jsonipc gpiozero
```

## Image Gallery

![First button press sequence](/Documentation/images/readme/1.jpeg)
![Reverse I/O panel](/Documentation/images/readme/2.jpeg)
![Photoshoot](/Documentation/images/readme/3.jpeg)
![Ham radio headset](/Documentation/images/readme/4.jpeg)
![Second sequence](/Documentation/images/readme/5.jpeg)
![Third sequence](/Documentation/images/readme/6.jpeg)
![Shutdown](/Documentation/images/readme/7.jpeg)

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contact

For any inquiries or issues, please reach out to [Halophilus](email:benshaw@halophil.us).

## Acknowledgments

Special thanks to Ethan McCue for the development of the looping_video.py script.
