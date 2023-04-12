import subprocess
import json

def get_video_duration(file_path):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        file_path,
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        output = json.loads(result.stdout)
        duration = float(output["format"]["duration"])
        return duration
    except (KeyError, ValueError):
        print(f"Error: Could not retrieve the duration of the video '{file_path}'")
        return None

if __name__ == "__main__":
    video_file = "C:\\Users\\Thomas.Henshaw001\\Development\\Ouch!\\VideoMaker\\Videos\\BOOT.mp4"
    duration = get_video_duration(video_file)
    if duration:
        print(f"Video duration: {duration} seconds")
