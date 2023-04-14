import vlc
import time
import threading

class VLCVideoPlayer:
    def __init__(self, video_list=[],file_path=None):
        self.player = None
        self.video_list = video_list
        self.section_dict = None
        self.section_index_list = None
        self.stop_loop = False
        self.current_thread = None
        self.stop_loop_event = threading.Event()

        if file_path is not None:
            self.play_video(file_path)
        
        if self.video_list is not None:
            self.section_dict = self.create_section_dictionary(self.video_list)
            self.section_index_list = self.create_section_index_list(self.video_list)
    
    def create_section_dictionary(sections):
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
        first_video = self.section_index_list[0]
        first_video = self.section_dict[first_video]
        self.play_section(first_video)

    def play_video_from_time_point(self, time_point):
        if self.player is None:
            print("No video!")
            return
        if self.player.get_state() in [vlc.State.Playing, vlc.State.Paused]:
            # Convert time_point to milliseconds and set the player's time
            self.player.set_time(int(time_point * 1000))
        else:
            print("Out of range!")

    def play_section(self, section_name):
        if section_name not in self.section_dict:
            print("Section not found!")
            return

        # Stop the current loop
        self.stop_loop = True
        self.stop_loop_event.wait()  # Wait for the section_loop to signal that it has stopped

        if self.current_thread is not None:
            self.current_thread.join()

        # Reset the stop_loop flag and the stop_loop_event
        self.stop_loop = False
        self.stop_loop_event.clear()

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

    def create_section_index_list(self, sections):
        section_index_list = [section_name for section_name, _ in sections]
        return section_index_list

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
