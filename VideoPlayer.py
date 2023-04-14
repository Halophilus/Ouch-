import vlc
import time
import threading

class VLCLooper:
    def __init__(self, *, media, start_time, end_time):
        self._media = media
        self._start_time = start_time
        self._end_time = end_time
        self._kill = False
        self._task = None

    def start(self):
        if self._task:
            raise Exception("Already Started")
        else:
            self._task = threading.Thread(target=self._loop)
            self._task.start()

    def _loop(self):
        print("STARTING LOOP")
        self._media.set_time(self._start_time)
        while not self._kill:
            print("SETTING TIME")
            print("GOT TIME: " + self._media.get_time())
            print("END TIME: " + self._end_time)
            if self._media.get_time() >= self._end_time:
                self._media.set_time(self._start_time)
            time.sleep(0.1)

    def stop(self):
        self._kill = True
        self._task.join()
        self._task = None

class VLCVideoPlayer:
    def __init__(self, video_list=[],file_path=None):
        self.player = None
        self.video_list = video_list
        self.section_dict = None
        self.stop_loop = False

        if not self.video_list:
            raise Exception("Empty video list")
        if not file_path:
            raise Exception("No file path")
        
        self.section_dict = self.create_section_dictionary(self.video_list)
        self.play_video(file_path)
    
    def create_section_dictionary(self, sections):
        tracking_point = 0.0
        section_dict = {}

        for section in sections:
            section_name, duration = section
            section_dict[section_name] = (tracking_point, tracking_point + duration)
            tracking_point += duration

        return section_dict

    def play_video(self, file_path):
        instance = vlc.Instance("--no-xlib --no-osd --fullscreen --no-video-title-show")
        self.player = instance.media_player_new()
        media = instance.media_new(file_path)
        self.player.set_media(media)
        self.player.audio_output_set("analog")
        self.player.play()
        self.looper = VLCLooper(media=media, start_time = 0, end_time=3)
        self.looper.start()
        time.sleep(10000)
        #first_video = self.section_index_list[0]
        #first_video = self.section_dict[first_video]
        #self.play_section(first_video)

    def play_video_from_time_point(self, time_point):
        pass

    def play_section(self, section_name):
        if section_name not in self.section_dict:
            print("Section not found!")
            return

        # Reset the stop_loop flag and the stop_loop_event
        self.stop_loop = False

        def section_loop():
            start_time, end_time = self.section_dict[section_name]
            duration_in_tenths = (end_time - start_time) * 10.0
            while not self.stop_loop:
                self.play_video_from_time_point(start_time)
                for _ in range(duration_in_tenths):
                    if self.stop_loop:
                        return
                    time.sleep(0.1)

            self.stop_loop_event.set()  # Signal that the section_loop has stopped

        # Start the loop in a background thread
        self.current_thread = threading.Thread(target=section_loop)
        self.current_thread.start()

    def stop(self):
        # Stop the current section loop if it's running
        self.stop_loop = True
        self.stop_loop_event.wait()

        if self.current_thread is not None:
            self.current_thread.join()

        # Reset the stop_loop flag and the stop_loop_event
        self.stop_loop = False
        self.stop_loop_event.clear()

        # Pause the video and set its position to the very beginning
        if self.player is not None:
            self.player.pause()
            self.player.set_time(0)
