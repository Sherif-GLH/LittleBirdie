import os
import requests
import boto3
from moviepy import *
from io import BytesIO
from datetime import datetime
from .LittleBirdie.RepeatedVideo import repeat_video
from .LittleBirdie.Transcript import adding_transcripts_audio
from .LittleBirdie.RepeatedAudio import adding_background_audio
from .LittleBirdie.ImageTransition import image_transition, video_transition

def create_video(intro, transcript_audio, content, video_name):
    background_video = VideoFileClip('downloads/BG Template.mp4')
    background_audio = AudioFileClip('downloads/music.mp3')
    intro_video = VideoFileClip('downloads/intro.mp4')
    outro_video = VideoFileClip('downloads/outro.mp4')
    w, h = background_video.size
    audio_clips1 = []
    audio_clips2 = []
    speed = 800 
    clips = []
    audio_clips = []
    total_duration = 0
    new_start_time = 0
    for item in intro: 
        media_path = item["url"]
        file_extension = os.path.splitext(media_path)[1].lower()
        if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', 'webp']:
            pause_duration = item["pause_duration"]
            response = requests.get(media_path)
            image_data = BytesIO(response.content)
            total_duration, clips = image_transition(image_data, total_duration, clips, new_start_time, pause_duration, w, h, speed)
        elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
            audio = item["with_audio"]
            total_duration, clips, audio_clips1 = video_transition(media_path, total_duration, clips, new_start_time, audio, audio_clips, w, h, speed)
        new_start_time = total_duration

    ## modify the duration of background video ##
    background_video_repeated = repeat_video(video=background_video, total_duration=total_duration)
    logo_image = ImageClip("downloads/WATERMARK.png").resized(width=150).with_position((1740,900)).with_duration(background_video_repeated.duration)
    clips.append(logo_image)
    video = CompositeVideoClip([background_video_repeated] + clips)
    video.write_videofile("downloads/video1.mp4", fps=30)

    clips = []
    total_duration = 0
    audio_clips = []
    new_start_time = 0

    for item in content:
        media_path = item["url"]
        file_extension = os.path.splitext(media_path)[1].lower()
        if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
            pause_duration = item["pause_duration"]
            response = requests.get(media_path)
            image_data = BytesIO(response.content)
            total_duration, clips = image_transition(image_data, total_duration, clips, new_start_time, pause_duration,w, h, speed)
        elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
           audio = item["with_audio"]
           total_duration, clips, audio_clips2 = video_transition(media_path, total_duration, clips, new_start_time, audio, audio_clips,w, h, speed)
        new_start_time = total_duration

    background_video_repeated = repeat_video(video=background_video,total_duration=total_duration)
    logo_image = ImageClip("downloads/WATERMARK.png").resized(width=150).with_position((1740,900)).with_duration(background_video_repeated.duration)
    clips.append(logo_image)
    video = CompositeVideoClip([background_video_repeated] + clips)
    video.write_videofile("downloads/video2.mp4", fps=30)

    video1 = VideoFileClip("downloads/video1.mp4")
    video2 = VideoFileClip("downloads/video2.mp4")
    final_video = concatenate_videoclips([video1, intro_video, video2])
    final_with_outro = CompositeVideoClip([final_video, outro_video.with_effects([vfx.SlideIn(0.3, "top")]).with_start(final_video.duration - 1)]).subclipped()
    background_audio = background_audio.subclipped(0,final_with_outro.duration)
    background_audio = adding_background_audio(video1, intro_video, final_with_outro, audio_clips1, audio_clips2, background_audio)
    transcript_audio = adding_transcripts_audio(transcript_audio)
    combined_audio = CompositeAudioClip([transcript_audio, final_video.audio, background_audio])
    final = final_with_outro.with_audio(combined_audio)
    final.write_videofile("downloads/output1.mp4", fps=30)
    path = upload_to_s3("downloads/output1.mp4", f"LittleBirdie/{video_name}.mp4")
    return path

def upload_to_s3(file_path, s3_path):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_path,
                       ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded {file_path} to S3 bucket.")
        remove_local_file(file_path)
        remove_local_file("downloads/video1.mp4")
        remove_local_file("downloads/video2.mp4")
        remove_local_file("downloads/sample.mp3")
        remove_local_file("downloads/sample.mp4")
        return s3_path
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {str(e)}")

def remove_local_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed local file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")
