import vlc
import time

# Initialize VLC instance
instance = vlc.Instance("--no-xlib", "--vout=mmal_vout")


# Create a media player object
player = instance.media_player_new()

# Load the media (replace 'path/to/your/video.mp4' with the actual file path)
media = instance.media_new('/home/pi/Ouch-/master.mp4')

# Set the media to the player instance
player.set_media(media)

# Play the video
player.play()

# Wait for the video to start playing
time.sleep(1)

# Jump to the 10th second while the video is playing
player.set_time(10000)

# Wait for 5 seconds
time.sleep(5)

# Jump to the 30th second (30,000 milliseconds) while the video is still playing
player.set_time(30000)

# Wait for 10 seconds before stopping the video
time.sleep(10)

# Stop the video
player.stop()
