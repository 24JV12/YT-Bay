import yt_dlp
import os
import sys

def close():
    sys.exit(0)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

download_dir = ""

def change_download_path(new_download_dir):
    try:
        os.chdir(new_download_dir)
        print(f"Download path changed to: {new_download_dir}")
    except FileNotFoundError:
        print(f"Error: Directory {new_download_dir} not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

ffmpeg_path = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"

def flashlight():
    manual = [
        "cls          clear screen",
        "help         print out helping prompts",
        "exit         exit the program",
        "downcd       change download path",
        "downpath     prints the path of the download dir"
    ]
    for entry in manual:
        print(entry)

def get_ydl_opts():
    return {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }, {
        'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path
    }

def list_formats(url):
    ydl_opts = {
        'listformats': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error listing formats: {str(e)}")

def download(url):
    format = input("FORMAT? (V/A): ").upper()
    ydl_opts_video, ydl_opts_audio = get_ydl_opts()
    try:
        if format in ["V", "VID", "VIDEO"]:
            with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
                ydl.download([url])
        elif format in ["A", "AUD", "AUDIO"]:
            with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download([url])
        else:
            print("Invalid format. Please enter 'V' for video or 'A' for audio.")
    except Exception as e:
        print(f"Download error: {str(e)}")
        print("Listing available formats...")
        list_formats(url)

if not download_dir:
    download_dir = input("Where would you like to save the media from YouTube? ")
    try:
        os.chdir(download_dir)
    except FileNotFoundError:
        print(f"Error: Directory {download_dir} not found.")
        sys.exit(1)

if not ffmpeg_path:
    ffmpeg_path = input("Where is ffmpeg.exe stored? (use double backslashes) ")

while True:
    command = input("URL or COMMAND: ")
    if command.lower() == "cls":
        clear()
    elif command.lower() == "exit":
        close()
    elif command.lower().startswith("downcd"):
        try:
            new_path = command.split(" ", 1)[1]
            change_download_path(new_path)
        except IndexError:
            print("Please provide a new download path.")
    elif command.lower() == "help":
        flashlight()
    elif command.lower() == "downpath":
        current_dir = os.getcwd()
        print(current_dir)
    else:
        download(command)
