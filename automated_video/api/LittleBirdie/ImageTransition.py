from moviepy import *
from PIL import Image
import requests
from .EditingOnImage import process_image_height, process_image_width
def scaling_image(t,time_to_center):
    if t <= time_to_center:
        return 1
    else:
        return (1 + ((t-time_to_center)*0.06))

def move_image(t, start_pos, center_pos, time_to_ctr, pause_dur, w, h):
    if t <= 0:
        return start_pos
    elif 0 < t <= time_to_ctr:
        new_height = start_pos[1] - (t * (start_pos[1] - center_pos[1]) / time_to_ctr)
        return (start_pos[0], new_height)
    elif time_to_ctr <= t < time_to_ctr + pause_dur:
        return ("center", "center")
    else:
        return (w, h)

def image_transition(image_path, total_duration, clips, new_start_time, pause_duration, w, h, speed): 
    print("enter image transition")
    image = Image.open(image_path)
    image_width, image_height = image.size
    if abs(image_width - image_height) > 100:
        if image_height > image_width:
            process_image_height(image_path, "temp/final_output.png", target_height=650)
            image_clip = ImageClip("temp/final_output.png")
            start_position = ("center", (h /2)-300)
            center_position = ("center", abs((h / 2) - (image_clip.h / 2)))
        else:
            process_image_width(image_path, "final_output.png", target_width=900)
            image_clip = ImageClip("final_output.png")
            start_position = ("center", (h /2)-100)
            center_position = ("center", abs((h / 2) - (image_clip.h / 2)))
    else:
        process_image_width(image_path, "final_output.png", target_width=600)
        image_clip = ImageClip("final_output.png")
        start_position = ("center", (h /2)-100)
        center_position = ("center", abs((h / 2) - (image_clip.h / 2)))
    print("finishing processing image")
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    
    # Bind the current iteration's variables
    animated_image = (
        image_clip
        .with_position(lambda t, sp=start_position, cp=center_position,
                       time_to_ctr=time_to_center, pause_dur=pause_duration
                         : move_image(t, sp, cp, time_to_ctr, pause_dur, w, h))
        .with_start(new_start_time)
        .with_duration(pause_duration)
        .resized(lambda t : scaling_image(t,time_to_center))
    )
    animated_image = animated_image.with_effects([vfx.CrossFadeIn(0.2)])
    clips.append(animated_image)
    total_duration += animated_image.duration
    return total_duration, clips

def video_transition(i, video_path, total_duration, clips, new_start_time, audio, audio_clips, w, h, speed):
    print("entering video transition")
    local_filename = f"temp/sample{i}.mp4"

    # Perform the GET request and download the file
    response = requests.get(video_path, stream=True)
    response.raise_for_status()  # Check for HTTP errors
    with open(local_filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
            file.write(chunk)
    video_clip = VideoFileClip(local_filename)
    pause_duration = video_clip.duration
    # audio clips
    if not audio:
        video_clip = video_clip.without_audio()
    else:
        audio_clip = (new_start_time, new_start_time+pause_duration)
        audio_clips.append(audio_clip)
    # Extract the first frame
    frame_width, frame_height = video_clip.w, video_clip.h
    print("enerting process of video" )
    if frame_height > frame_width:
        video_clip = video_clip.resized(height=850)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("temp/final_output.png")
        frame_image = "temp/final_output.png"
        
        process_image_height(frame_image, "temp/final_output.png", target_height=850)
        frame_image = ImageClip("temp/final_output.png")
        start_position = (721, (h /2)-300)
        shadow_position = (721-21, start_position[1]-12)
        shadow_center = (721-21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = (721, abs((h / 2) - (frame_image.h / 2)))
    else:
        video_clip = video_clip.resized(width=1080)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("temp/final_output.png")
        frame_image = "temp/final_output.png"
        process_image_width(frame_image, "temp/final_output.png", target_width=1080)
        frame_image = ImageClip("temp/final_output.png")
        start_position = ("center", (h /2)-100)
        shadow_position = (420-21, start_position[1]-12)
        shadow_center = (420 -21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = ("center", abs((h / 2) - (frame_image.h / 2)))
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    print("animating the video")

    # animating shadow
    shadow = ImageClip("temp/final_output.png")
    animated_shadow = (
    shadow 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=shadow_position, cp=shadow_center,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_image(t, sp, cp, time_to_ctr, pause_dur, w, h))
    )
    animated_shadow = animated_shadow.with_effects([vfx.CrossFadeIn(0.2)])
    animated_video = (
    video_clip 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=start_position, cp=center_position,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_image(t, sp, cp, time_to_ctr, pause_dur, w, h))
    )
    animated_video = animated_video.with_effects([vfx.CrossFadeIn(0.2)])
    clips.append(animated_shadow)
    clips.append(animated_video)
    print(animated_video.duration)
    total_duration += animated_video.duration
    return total_duration, clips, audio_clips
