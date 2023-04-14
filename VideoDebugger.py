import vlc
import time

# Initialize VLC instance
instance = vlc.Instance("--no-xlib", "--vout=mmal_vout")


# Create a media player object
player = instance.media_player_new()

# Load the media (replace 'path/to/your/video.mp4' with the actual file path)
media = instance.media_new('/home/pi/Ouch-/master.mp4')

# Set the media to the player instance
player.set_media(media)

# Play the video
player.play()

# Wait for the video to start playing
time.sleep(1)

# Jump to the 10th second while the video is playing
player.set_time(10000)

# Wait for 5 seconds
time.sleep(5)

# Jump to the 30th second (30,000 milliseconds) while the video is still playing
player.set_time(30000)

# Wait for 10 seconds before stopping the video
time.sleep(10)

# Stop the video
player.stop()
import os
import subprocess
import time

class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.player = None

    def play(self):
        self.player = subprocess.Popen(['omxplayer', '--no-osd', self.video_path],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)

    def jump_to_timestamp(self, timestamp):
        if self.player is None:
            print("Please start the video using the play() method before using jump_to_timestamp.")
            return

        jump_cmd = f"{timestamp}\n"
        self.player.stdin.write(jump_cmd)
        self.player.stdin.flush()

    def stop(self):
        if self.player is not None:
            self.player.stdin.write('q\n')
            self.player.stdin.flush()
            self.player.wait()
            self.player = None

# Usage example
video_path = "/home/pi/Ouch-/master.mp4"
player = VideoPlayer(video_path)

# Play the video
player.play()
time.sleep(5)

# Jump to a specific timestamp (in seconds)
player.jump_to_timestamp(30)
time.sleep(5)
player.jump_to_timestamp(30)
time.sleep(5)
player.jump_to_timestamp(45)
time.sleep(5)
player.jump_to_timestamp(30)
time.sleep(5)
# Stop the video playback
player.stop()
