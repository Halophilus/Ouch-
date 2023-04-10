import subprocess
import time
import threading


class OMXPlayerEngine:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.current_index = 0
        self.omxplayer_process = None
        self.loop_video = True
        self.video_loop_thread = None

    def _loop_video(self):
        while self.loop_video:
            if self.omxplayer_process is not None and self.omxplayer_process.poll() is not None:
                self.play_video(self.current_index)
            time.sleep(0.5)

    def play_video(self, index):
        if self.omxplayer_process is not None and self.omxplayer_process.poll() is None:
            self.omxplayer_process.terminate()
            time.sleep(0.5)

        if 0 <= index < len(self.video_paths):
            self.current_index = index
            video_path = self.video_paths[self.current_index]
            self.omxplayer_process = subprocess.Popen(
                [
                    "omxplayer",
                    "--no-osd",
                    "--no-keys",
                    "-b",
                    "--adev",
                    "local",
                    video_path,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if self.video_loop_thread is None:
                self.video_loop_thread = threading.Thread(target=self._loop_video)
                self.video_loop_thread.start()
        else:
            print(f"Error: Invalid index {index}. Video not found.")

    def next_video(self):
        self.current_index += 1
        if self.current_index >= len(self.video_paths):
            self.current_index = 0
        self.play_video(self.current_index)

    def reset_sequence(self):
        self.current_index = 0


if __name__ == "__main__":
    video_player = OMXPlayerEngine(["video1.mp4", "video2.mp4", "video3.mp4"])

    # Play the video at index 1
    video_player.play_video(1)
    time.sleep(10)  # Wait for 10 seconds

    # Play the next video in the list
    video_player.next_video()
    time.sleep(10)  # Wait for 10 seconds

    # Reset the sequence and play the first video
    video_player.reset_sequence()
    video_player.play_video(0)
    time.sleep(10)  # Wait for 10 seconds
