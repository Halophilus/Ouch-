import dataclasses
import python_mpv_jsonipc
import typing

class LoopingVideo:
    @dataclasses.dataclass(frozen=True)
    class Segment:
        start: typing.Union[int, str]
        stop: typing.Union[int, str]

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

    def play_segment(self, *, segment_name):
        if self._mpv is None:
            raise Exception('Not started')

        segment = self._segments[segment_name]
        self._mpv.command('seek', segment.start, 'absolute')
        self._mpv.command('set', 'ab-loop-a', str(segment.start))
        self._mpv.command('set', 'ab-loop-b', str(segment.stop))
    
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
        )
    })

    print("FIRST SEGMENT")
    looping.start(initial_segment_name='initial_boot')
    time.sleep(10)
    print("SECOND SEGMENT")
    looping.play_segment(segment_name='sequence_1')

