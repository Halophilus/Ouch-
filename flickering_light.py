import time, random, threading

class FlickeringLight:
    '''
        Class definition for background LED flickering control without interrupting the flow of the code
        Attributes:
            _led (LED), gpiozero LED object
            _kill (bool), breaks flickering thread
            _freq (float), flickering frequency per second
            _thread (Thread), thread in which the flickering is manages
        Methods:
            _activity (internal helper function)
                Args: None
                Function: Handles flickering behavior with kill switch functionality
            start (global)
                Args: None
                Function: Starts a flickering thread if there is none, does nothing if there is
            stop (global)
                Args: None
                Function: Kills existing thread
            freq (property, getter):
                Returns the current flicker frequency for the object
            freq (setter)
                Replaces existing flicker frequency
    '''
    def __init__(self, *, led, freq=2):
        self._led = led
        self._kill = False
        self._freq = freq
        self._thread = None

    def _activity(self):
        try:
            while True:
                print("L", flush=True)
                if self._kill:
                    self._thread = None
                    break
                time.sleep(random.uniform(0,self._freq))
                self._led.on()
                time.sleep(random.uniform(0, self._freq/2))
                self._led.off()
        except Exception as e:
            print(e, flush=True)
            self._activity()

    def start(self):
        if self._thread is not None:
            raise Exception("Already started")

        self._thread = threading.Thread(
            target = self._activity, 
            daemon = True
        )
        self._thread.start()
    
    def stop(self):
        self._kill = True

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, new_freq):
        self._freq = new_freq
