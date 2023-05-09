import time
import random
import threading

class FlickeringLight:
    def __init__(self, *, led, freq=2):
        self._led = led
        self._kill = False
        self._freq = freq
        self._thread = None

    def _activity(self):
        while True:
            if self._kill:
                self._thread = None
                break
            time.sleep(random.uniform(0,self._freq))
            self._led.on()
            time.sleep(random.uniform(0, self._freq/2))
            self._led.off()

    def start(self):
        if self._thread is not None:
            raise Exception("Already started")

        self._thread = threading.Thread(
            target = self._activity, 
            daemon = True
        )
    
    def stop(self):
        self._kill = True

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, new_freq):
        self._freq = new_freq

if __name__ == '__main__':
    import gpiozero

    flickering = FlickeringLight(
        led=gpiozero.LED(10)
    )
    
    flickering.start()

    time.sleep(10)

    flickering.freq = 0.5

    time.sleep(5)

    flickering.freq = 0.25

    time.sleep(5)

    flickering.stop()

    print("DONE")