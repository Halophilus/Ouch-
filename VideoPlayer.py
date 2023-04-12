import subprocess
import time
import threading

class VLCSectionLooper:
    def __init__(self, video_sections, master_video):
        self.video_sections = video_sections
        self.master_video = master_video
        self.current_index = 0
        self._vlc_process = None
        self._playback_thread = None
        self._stop_playback_thread = threading.Event()

        self._vlc_process = subprocess.Popen(
            [
                "cvlc",
                "--no-osd",
                "--no-xlib",
                "--fullscreen",
                "--no-video-title-show",
                "--aout=alsa",
                "--alsa-audio-device=hw:1,0",
                "--loop",
                self.master_video
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(2)  # Allow some time for VLC to start
        self.play_video(self.current_index)

    def _get_video_start_end(self, index):
        start_time = sum(video[1] for video in self.video_sections[:index])
        end_time = start_time + self.video_sections[index][1]
        return start_time, end_time

    def _play_video_section(self, index):
        start_time, end_time = self._get_video_start_end(index)
        while not self._stop_playback_thread.is_set():
            self._vlc_process.stdin.write(f"seek {start_time}\n".encode())
            self._vlc_process.stdin.flush()
            time.sleep(self.video_sections[index][1])

    def play_video(self, index):
        if 0 <= index < len(self.video_sections):
            self.current_index = index
            self._stop_playback_thread.set()

            if self._playback_thread is not None:
                self._playback_thread.join()

            self._stop_playback_thread.clear()
            self._playback_thread = threading.Thread(target=self._play_video_section, args=(self.current_index,))
            self._playback_thread.start()
        else:
            print(f"Error: Invalid index {index}. Video not found.")

    def next_video(self):
        self.current_index += 1
        if self.current_index >= len(self.video_sections):
            self.current_index = 0
        self.play_video(self.current_index)

    def reset_sequence(self):
        self.current_index = 0

    def get_current_video(self):
        return self.video_sections[self.current_index][0]

    def stop(self):
        self._stop_playback_thread.set()
        if self._playback_thread is not None:
            self._playback_thread.join()
        if self._vlc_process is not None:
            self._vlc_process.stdin.write(b"quit\n")
            self._vlc_process.stdin.flush()
            self._vlc_process.wait()

video_sections = [("Section 1", 10), ("Section 2", 12), ("Section 3", 15)]
master_video = "concatenated_video.mp4"
video_player = VLCSectionLooper(video_sections, master_video)

time.sleep(10)
video_player.play_video(1)
print("Currently playing:", video_player.get_current_video())
time.sleep(10)

video_player.next_video()
time.sleep(10)

video_player.reset_sequence()
video_player.play_video(0)
time.sleep(10)

video_player.stop()
