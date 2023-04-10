import os
import time
from omxplayer.player import OMXPlayer
from pathlib import Path

class InteractiveVideoPlayer:
    def __init__(self, video_files, audio_output="local"):
        self.video_files = video_files
        self.current_video_index = 0
        self.audio_output = audio_output
        self.player = None

    def play_video(self, video_index=None):
        if video_index is not None:
            self.current_video_index = video_index

        video_path = self.video_files[self.current_video_index]
        if self.player is not None:
            self.player.quit()

        self.player = OMXPlayer(video_path, args=['--loop', '--no-osd', f'--adev={self.audio_output}'])
        self.player.set_video_pos(0, 0, 1920, 1080)

    def next_video(self):
        self.current_video_index += 1
        if self.current_video_index >= len(self.video_files):
            self.current_video_index = 0

        self.play_video()

    def reset_sequence(self):
        self.current_video_index = 0
        self.play_video()

if __name__ == "__main__":
    video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]
    ivp = InteractiveVideoPlayer(video_files)

    # Play the first video
    ivp.play_video()

    # Wait and then play the next video
    time.sleep(10)
    ivp.next_video()

    # Wait and then reset the sequence
    time.sleep(10)
    ivp.reset_sequence()
