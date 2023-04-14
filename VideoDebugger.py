import vlc
import time

def vlc_log_handler(data, level, ctx, fmt, args):
    msg = fmt % args
    print("[VLC] %s" % msg)

# Initialize VLC instance with log handler
instance = vlc.Instance()
instance.log_set(vlc_log_handler, None)

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

# Check if the video is playing
if player.get_state() == vlc.State.Playing:
    # Set the time to 10 seconds (10,000 milliseconds)
    player.set_time(10000)
    print("Successfully set the time to 10 seconds.")
else:
    print("Video is not playing yet.")

# Wait for 10 seconds before stopping the video
time.sleep(10)

# Stop the video
player.stop()
