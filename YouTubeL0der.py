import yt_dlp
import colorama
import os
from colorama import Fore, Style
import requests
import re

colorama.init(autoreset=True)

def print_ascii_art():
    print(Fore.CYAN + '''
__   _______ _  ___            _           
\ \ / /_   _| |/ _ \  __ _  __| | ___ _ __ 
 \ V /  | | | | | | |/ _` |/ _` |/ _ \ '__|
  | |   | | | | |_| | (_| | (_| |  __/ |   
  |_|   |_| |_|\___/ \__,_|\__,_|\___|_|   
''' + Style.RESET_ALL)

def print_completion_art():
    print(Fore.CYAN + '''
  ____           ___                    
| __ ) _   _   / _ \ _ __  _ __   __ _ 
|  _ \| | | | | | | | '_ \| '_ \ / _` |
| |_) | |_| | | |_| | |_) | | | | (_| |
|____/ \__, |  \___/| .__/|_| |_|\__, |
       |___/        |_|          |___/  
''' + Style.RESET_ALL)

DEFAULT_VIDEO_FORMAT = 'bestvideo[ext=mp4][height<=1080][fps=60]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]'
SEPARATE_VIDEO_AUDIO_FORMAT = 'bestvideo[ext=mp4][height<=1080][fps=60]'

def sanitize_filename(filename):
    """
    Sanitizes a filename by removing special characters and limiting the length.
    """
    MAX_FILENAME_LENGTH = 100
    sanitized_filename = re.sub(r'[^\w\-_\. ]', '_', filename)
    return sanitized_filename[:MAX_FILENAME_LENGTH]

def download_video_and_thumbnail(url, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)

    video_title = sanitize_filename(yt_dlp.YoutubeDL().extract_info(url, download=False).get('title'))
    output_folder = os.path.join(output_directory, video_title)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    download_separately = input(Fore.RED + "你要把影片(mp4)和音頻(m4a)分開儲存嗎？ [y/n] " + Style.RESET_ALL)
    if download_separately.lower() == 'y':
        ydl_opts = {
            'outtmpl': os.path.join(output_folder, '%(title)s_video.%(ext)s'),
            'format': SEPARATE_VIDEO_AUDIO_FORMAT
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                video_path = os.path.join(output_folder, f"{video_title}_video.mp4")
                print(Fore.GREEN + f"影片已成功下載：  {video_path}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error downloading video: {e}" + Style.RESET_ALL)

        ydl_opts = {
            'outtmpl': os.path.join(output_folder, '%(title)s_audio.%(ext)s'),
            'format': 'bestaudio[ext=m4a]'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                audio_path = os.path.join(output_folder, f"{video_title}_audio.m4a")
                print(Fore.GREEN + f"音檔已成功下載： {audio_path}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error downloading audio: {e}" + Style.RESET_ALL)
    else:
        ydl_opts = {
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'format': DEFAULT_VIDEO_FORMAT
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                video_path = os.path.join(output_folder, f"{video_title}.mp4")
                print(Fore.GREEN + f"Video downloaded: {video_path}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error downloading video: {e}" + Style.RESET_ALL)

    download_thumbnail = input(Fore.RED + "你要下載影片封面/縮圖嗎？ [y/n] " + Style.RESET_ALL)
    if download_thumbnail.lower() == 'y':
        thumbnail_path = os.path.join(output_folder, f"{video_title}.jpg")
        thumbnail_url = yt_dlp.YoutubeDL().extract_info(url, download=False).get('thumbnail')
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            with open(thumbnail_path, 'wb') as thumbnail_file:
                thumbnail_file.write(response.content)
            print(Fore.GREEN + f"封面已成功下載： {thumbnail_path}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Thumbnail URL not found." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "已取消封面下載" + Style.RESET_ALL)

def main():
    print_ascii_art()
    video_url = input(Fore.RED + "請輸入你要下載的影片網址： " + Style.RESET_ALL)
    output_directory = input(Fore.RED + "請輸入你要下載到的路徑： " + Style.RESET_ALL)

    download_video_and_thumbnail(video_url, output_directory)
    print(Fore.GREEN + "下載已完成！" + Style.RESET_ALL)

    print_completion_art()  # Call the new function here

if __name__ == "__main__":
    main()