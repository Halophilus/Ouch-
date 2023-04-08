import subprocess
import time

class OmxplayerPlayer:
    def __init__(self):
        self.process = None
        self.video_file = None
        self.is_playing = False
        self.default_image = "DEFAULT.png"
    
    def play(self, file_name, loop=False):
        if self.is_playing:
            self.stop()
        self.video_file = file_name
        loop_flag = "--loop" if loop else ""
        cmd = f"omxplayer -b --no-osd --aspect-mode stretch --adev alsa -o hdmi,alsa {loop_flag} './{file_name}'"
        self.process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
        self.is_playing = True

    def stop(self):
        if self.is_playing:
            self.process.stdin.write(b'q')
            self.process.stdin.flush()
            self.process.wait()
            self.is_playing = False
            self.video_file = None
            self.show_default_image()
    
    def get_time_remaining(self):
        if self.is_playing:
            cmd = ' '.join(['bash', '-c', f'echo "{chr(27)}[0;50;24M" | dd bs=1 count=4 2>/dev/null ; cat /proc/{self.process.pid}/stat | cut -d" " -f15'])
            time_remaining_ms = int(subprocess.check_output(cmd, shell=True))
            return time_remaining_ms / 1000
        return None
    
    def show_default_image(self):
        cmd = f"fbi -d /dev/fb0 -noverbose -a '{self.default_image}'"
        subprocess.call(cmd, shell=True)
        self.is_playing = False
    
    def set_default_image(self, image_path):
        self.default_image = image_path
        if not self.is_playing:
            self.show_default_image()

if __name__ == "__main__":
    player = OmxplayerPlayer()
    player.show_default_image()  # Show the default image at the beginning
    player.play("example.mp4", loop=True)
    time.sleep(10) # Wait for 10 seconds before stopping the player
    player.stop()
