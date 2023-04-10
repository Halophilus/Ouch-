import sys
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject

class InteractiveVideoPlayer:
    def __init__(self, video_files):
        self.video_files = video_files
        self.current_video_index = 0

        Gst.init(None)
        self.pipeline = Gst.Pipeline.new("interactive-video-player")

        self.source = Gst.ElementFactory.make("filesrc", "file-source")
        self.decodebin = Gst.ElementFactory.make("decodebin", "decoder")
        self.audioconvert = Gst.ElementFactory.make("audioconvert", "audio-convert")
        self.audioresample = Gst.ElementFactory.make("audioresample", "audio-resample")
        self.audiosink = Gst.ElementFactory.make("alsasink", "audio-output")
        self.audiosink.set_property("device", "hw:1,0") # Output audio to the 3.5mm jack
        self.videoconvert = Gst.ElementFactory.make("videoconvert", "video-convert")
        self.videosink = Gst.ElementFactory.make("autovideosink", "video-output")

        self.pipeline.add(self.source)
        self.pipeline.add(self.decodebin)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.audioresample)
        self.pipeline.add(self.audiosink)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.videosink)

        self.source.link(self.decodebin)
        self.audioconvert.link(self.audioresample)
        self.audioresample.link(self.audiosink)
        self.videoconvert.link(self.videosink)

        self.decodebin.connect("pad-added", self.on_pad_added)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_bus_call)
    
    def reset_sequence(self):
        self.current_video_index = 0

    def on_pad_added(self, element, pad):
        pad_type = pad.query_caps(None).to_string()
        if pad_type.startswith("audio"):
            pad.link(self.audioconvert.get_static_pad("sink"))
        elif pad_type.startswith("video"):
            pad.link(self.videoconvert.get_static_pad("sink"))

    def on_bus_call(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.play_next()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.stop()
        return True

    def play_next(self):
        self.current_video_index += 1
        if self.current_video_index >= len(self.video_files):
            self.current_video_index = 0
        self.play_video(self.video_files[self.current_video_index])

    def play_video(self, video_path):
        self.pipeline.set_state(Gst.State.NULL)
        self.source.set_property("location", video_path)
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.reset_sequence()

if __name__ == "__main__":
    video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]
    ivp = InteractiveVideoPlayer(video_files)
    ivp.play_video(video_files[0])

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ivp.stop()
