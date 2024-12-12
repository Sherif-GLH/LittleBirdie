import math 
from moviepy import * 

def repeat_video(video,total_duration):
    video_duration = video.duration
    if video_duration > total_duration:
        total_video = video.subclipped(0,total_duration)
        return total_video
    else: 
        repeated_times = total_duration / video_duration
        total_number = math.ceil(repeated_times)
        list_videos = []
        for number in range(0,total_number):
            video = (
                video
                .with_position((0,0))
                .resized(width=1920)
                .with_start(number*video_duration)
                .with_duration(video_duration)
                .with_fps(30)
                )
            list_videos.append(video)
        total_video = CompositeVideoClip(list_videos)
        total_video = total_video.subclipped(0,total_duration)
        return total_video