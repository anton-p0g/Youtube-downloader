from pytube import YouTube, Playlist
import os
import subprocess

path = "YouTube\\"
run = True

def download_streams(type, download_video, download_audio):
    stream_video = type.streams.filter(progressive=False, mime_type="video/webm", res=video_quality).first()
    stream_audio = type.streams.filter(progressive=False, type="audio", mime_type="audio/webm").last()
    filename = stream_video.default_filename    #Get the youtube's video title as filename
    
    if stream_video is not None:
        #Video
        if download_video == "video": 
            filename_video = f"{filename.split('.')[0]}_video.{filename.split('.')[1]}"  #Splits the filename into name and extension split by a .
            video_path = path + filename_video
            stream_video.download(path, filename_video)
    else: 
        print(f"No suitable video stream found for {type.title}")

    #Audio
    if stream_audio is not None:
        if download_audio == "audio":
            filename_audio = f"{filename.split('.')[0]}_audio.{filename.split('.')[1]}"
            audio_path = path + filename_audio   
            stream_audio.download(path, filename_audio) 
    else: 
        print(f"No suitable video stream found for {type.title}")
    
    output_path = path + filename

    if download_audio == "audio" and download_video == "video":
        command = ['C:/ffmpeg/bin/ffmpeg.exe', '-i', video_path, '-i', audio_path, '-c', 'copy', output_path]     #Combine the video and audio file into a single file using ffmpeg
        subprocess.run(command, shell=False)
        os.remove(video_path)
        os.remove(audio_path)

    print("Content downloaded!")

def download_options():
    global download_audio, download_video, video_quality
    download_audio = input("Download audio? (y/n) ")
    if download_audio == "y":
       download_audio = "audio" 
    
    download_video = input("Download video? (y/n) ")
    if download_video == "y":
       download_video = "video"
       video_quality = input("Enter desired video quality (144p, 240p, 360p, 720p, 1080p or 2160p) ")

while run:
    option = input("Download video or playlist? (v/p) ")

    if option == "v":
        link = input("Enter Youtube link: ")
        yt = YouTube(link)
        download_options()
        download_streams(yt, download_video, download_audio)

    elif option == "p": 
        playlist = Playlist(input("Enter a playlist link: "))
        download_options()
        
        for video in playlist.videos:
            download_streams(video, download_video, download_audio)
    else:
        print("Invalid input")

    run_again = input("\n\nDownload something else? (y/n) ")
    if run_again != "y":
        run = False