import yt_dlp # receives URL and then downloads the selected utube vids
import os #file/folder paths handling

# static_ffmpeg provides BOTH ffmpeg AND ffprobe (imageio_ffmpeg only has ffmpeg)
from static_ffmpeg import run as ffmpeg_run
FFMPEG_PATH, FFPROBE_PATH = ffmpeg_run.get_or_fetch_platform_executables_else_raise()
FFMPEG_DIR = os.path.dirname(FFMPEG_PATH)  # yt-dlp needs the directory containing both binaries

# Now import pydub and tell it where ffmpeg lives
from pydub import AudioSegment
AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # FFmpeg postprocessor converts it to WAV
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "ffmpeg_location": FFMPEG_DIR,  # yt-dlp looks for ffmpeg AND ffprobe in this directoryfgdfgfdvfdbfdb f
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename

if __name__ == "__main__":
    result = download_youtube_audio("https://www.youtube.com/watch?v=JgHkKNHv6tE&pp=0gcJCRsMAYcqIYzv")
    print("Downloaded:", result)