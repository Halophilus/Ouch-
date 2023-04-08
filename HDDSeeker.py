import os
import fcntl
import random
import time
import struct
import threading

# Constants for IOCTL commands
HDIO_DRIVE_CMD = 0x031f
WIN_SEEK = 0x70
HDIO_GETGEO = 0x0301

class HDDNoiseGenerator:
    def __init__(self, device_path):
        self.device_path = device_path
        self.fd = None
        self.noise_thread = None
        self.stop_event = threading.Event()

        self.intensity = 50
        self.geometry = None

    def open_drive(self):
        self.fd = os.open(self.device_path, os.O_RDWR | os.O_NONBLOCK)
        self.geometry = self.get_drive_geometry()

    def close_drive(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def get_drive_geometry(self):
        geo_struct = struct.Struct("H8xH")
        result = fcntl.ioctl(self.fd, HDIO_GETGEO, bytearray(geo_struct.size))
        cylinders, heads = geo_struct.unpack(result)
        return {"cylinders": cylinders, "heads": heads}

    def _generate_seeking_noise(self):
        while not self.stop_event.is_set():
            random_cylinder = random.randint(0, self.geometry["cylinders"] - 1)
            random_head = random.randint(0, self.geometry["heads"] - 1)

            command = bytearray([WIN_SEEK, 0, (random_cylinder >> 8) & 0xFF, random_cylinder & 0xFF, random_head])
            fcntl.ioctl(self.fd, HDIO_DRIVE_CMD, command)

            time.sleep(self._calculate_seek_duration())

    def _calculate_seek_duration(self):
        return (1.0 - self.intensity / 100.0) * 0.2

    def start(self):
        self.stop_event.clear()
        self.open_drive()

        self.noise_thread = threading.Thread(target=self._generate_seeking_noise)
        self.noise_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.noise_thread:
            self.noise_thread.join()
            self.noise_thread = None

        self.close_drive()

    def set_intensity(self, intensity):
        self.intensity = max(0, min(100, intensity))

def main():
    device_path = "/dev/sdX"  # Replace "sdX" with your device's identifier (e.g., sda, sdb, etc.)

    noise_generator = HDDNoiseGenerator(device_path)

    print("Starting HDD noise generation...")
    noise_generator.start()

    # Example usage: adjust the intensity of the HDD noise every 10 seconds
    for i in range(0, 110, 10):
        print(f"Setting intensity to {i}...")
        noise_generator.set_intensity(i)
        time.sleep(10)

    print("Stopping HDD noise generation...")
    noise_generator.stop()

if __name__ == "__main__":
    main()
