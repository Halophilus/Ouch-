import dataclasses
import python_mpv_jsonipc
import typing
import time

class LoopingVideo:
    @dataclasses.dataclass(frozen=True)
    class Segment:
        start: typing.Union[int, str]
        stop: typing.Union[int, str]


        @property
        def start_in_seconds(self):
            if isinstance(self.start, int):
                return self.start

            min, sec = self.start.split(':')
            return int(min) * 60 + int(sec)

        @property
        def stop_in_seconds(self):
            if isinstance(self.stop, int):
                return self.stop

            min, sec = self.stop.split(':')
            return int(min) * 60 + int(sec)

    def __init__(self, *, filepath, segments):
        self._filepath = filepath
        self._segments = segments
        self._mpv = None

    def start(self, *, initial_segment_name):
        if self._mpv is not None:
            raise Exception('Already started')
        
        initial = self._segments[initial_segment_name]
        self._mpv = python_mpv_jsonipc.MPV(**{ 
            'fullscreen': True,
            'ab-loop-a': str(initial.start),
            'ab-loop-b': str(initial.stop),
            'start': str(initial.start)
        })
        self._mpv.play(self._filepath)

    def skip_to_start(self, *, segment_name):
        if self._mpv is None:
            raise Exception('Not started')

        segment = self._segments[segment_name]
        self._mpv.command('seek', segment.start, 'absolute')

    def loop_segment_later(self, *, segment_name):
        if self._mpv is None:
            raise Exception('Not started')

        segment = self._segments[segment_name]
        self._mpv.command('set', 'ab-loop-a', str(segment.start))
        self._mpv.command('set', 'ab-loop-b', str(segment.stop))

    def wait_for_segment_to_be_reached(self, *, segment_name):
        if self._mpv is None:
            raise Exception('Not started')

        segment = self._segments[segment_name]

        while True:
            time.sleep(0.15)
            if segment.start_in_seconds < float(self._mpv.time_pos):
                return
    
if __name__ == '__main__':
    import time

    print("STARTING")
    looping = LoopingVideo(filepath='./video.mp4_new_audio.mp4', segments={
        'initial_boot': LoopingVideo.Segment(
            start=0,
            stop=40 # 40.791
        ),
        'sequence_1': LoopingVideo.Segment(
            start=41, # 40.791
            stop="1:45" # 01:45:166
        ),
        'transition_1': LoopingVideo.Segment(
            start="1:46", # 01:46:166
            stop="2:16" # 02:16:541
        ),
        'button_1': LoopingVideo.Segment(
            start='2:17',# 02:16:541
            stop='2:40' # 02:40:291
        ),
        'sequence_2': LoopingVideo.Segment(
            start='2:41',# 02:40:291
            stop='9:02' # 09:02:041
        ),
        'transition_2': LoopingVideo.Segment(
            start='9:02', # 09:02:041
            stop='10:22' # 10:22:583
        ),
        'button_2': LoopingVideo.Segment(
            start='10:23', # 10:22:583
            stop='10:43' # 10:43:458
        ),
        'sequence_3': LoopingVideo.Segment(
            start='10:44', # 10:43:458
            stop='18:15' # 18:15:166
        ),
        'transition_3': LoopingVideo.Segment(
            start='18:15', # 18:15:166
            stop='18:28' # 18:28:708
        ),
        'button_3': LoopingVideo.Segment(
            start='18:29', # 18:28:708
            stop='18:55' # 18:55:708
        ),
        'title_card': LoopingVideo.Segment(
            start='18:56', # 18:55:708
            stop='19:14' # 19:14:791
        ),
        'credits': LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:50:625
        ),
        'shutdown_screen': LoopingVideo.Segment(
            start='19:14', # 19:14:791
            stop='20:50' # 20:55:958
        )
    })

    print("FIRST SEGMENT")
    looping.start(initial_segment_name='initial_boot')
    time.sleep(1)
    print("SECOND SEGMENT")
    looping.skip_to_start(segment_name='sequence_1')
    looping.loop_segment_later(segment_name='transition_1')
    looping.wait_for_segment_to_be_reached(segment_name='transition_1')

