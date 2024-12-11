from moviepy import *
from PIL import Image, ImageFilter, ImageOps
import numpy as np
from RepeatBackground import repeat_video
import os
import requests
from io import BytesIO

def move_image(t, start_pos, center_pos, time_to_ctr, pause_dur):
            if t <= 0:
                return start_pos
            elif 0 < t <= time_to_ctr:
                new_height = start_pos[1] - (t * (start_pos[1] - center_pos[1]) / time_to_ctr)
                return (start_pos[0], new_height)
            elif time_to_ctr <= t < time_to_ctr + pause_dur:
                return center_pos
            else:
                return (w, h)

def add_borders_and_resize_width(image, target_width=1080):
    print("enetering add borders and resize" )
    # Resize the image to the target width, keeping the aspect ratio
    original_width, original_height = image.size
    scale_factor = target_width / original_width
    new_size = (target_width, int(original_height * scale_factor))
    resized_image = image.resize(new_size, Image.LANCZOS)  # Resize using high-quality filter
    
    # Add the first 1px gray border
    border1_color = (169, 169, 169)
    image_with_border1 = ImageOps.expand(resized_image, border=1, fill=border1_color)
    
    # Add the second 10px white border
    border2_color = (255, 255, 255)
    image_with_border2 = ImageOps.expand(image_with_border1, border=10, fill=border2_color)
    
    # Add the third 1px gray border
    image_with_border3 = ImageOps.expand(image_with_border2, border=1, fill=border1_color)
    
    return image_with_border3

def add_borders_and_resize_height(image, target_height=1080):
    print("enetering add borders and resize" )
    # Resize the image to the target height, keeping the aspect ratio
    original_width, original_height = image.size
    scale_factor = target_height / original_height
    new_size = (int(original_width * scale_factor), target_height)
    resized_image = image.resize(new_size, Image.LANCZOS)  # Resize using high-quality filter

    # Add the first 1px gray border
    border1_color = (169, 169, 169)
    image_with_border1 = ImageOps.expand(resized_image, border=1, fill=border1_color)
    
    # Add the second 10px white border
    border2_color = (255, 255, 255)
    image_with_border2 = ImageOps.expand(image_with_border1, border=10, fill=border2_color)
    
    # Add the third 1px gray border
    image_with_border3 = ImageOps.expand(image_with_border2, border=1, fill=border1_color)
    
    return image_with_border3

def add_drop_shadow(image, offset=(10, 10), shadow_color=(0, 0, 0, 128), blur_radius=10):
    print("enetering add drop shadow" )
    original = image.convert("RGBA")

    # Calculate the size of the new image (original + offset + blur)
    width, height = original.size
    total_width = width + abs(offset[0]) + blur_radius * 4
    total_height = height + abs(offset[1]) + blur_radius * 4

    # Create a transparent canvas
    transparent_canvas = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create the shadow layer
    shadow = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create a radial gradient for fading edges
    gradient = np.zeros((total_height, total_width), dtype=np.uint8)

    center_x = blur_radius * 2 + width // 2
    center_y = blur_radius * 2 + height // 2

    # Fill the gradient with fading opacity
    for y in range(total_height):
        for x in range(total_width):
            # Calculate the distance from the shadow center
            dist_x = abs(x - center_x)
            dist_y = abs(y - center_y)
            distance = max(dist_x - width // 2, dist_y - height // 2)

            # Compute alpha based on the distance
            if distance <= 0:
                alpha = 255  # Fully opaque in the central rectangle
            elif distance < blur_radius:
                alpha = 255 - int(255 * (distance / blur_radius))  # Fade out
            else:
                alpha = 0  # Fully transparent outside blur radius

            gradient[y, x] = alpha

    # Convert the gradient to an Image
    gradient_image = Image.fromarray(gradient, mode='L')

    # Paste the gradient on top of the shadow layer
    shadow.paste(shadow_color, (0, 0), mask=gradient_image)

    # Apply Gaussian blur to the shadow for smooth fading
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite the shadow onto the transparent canvas
    transparent_canvas = Image.alpha_composite(transparent_canvas, shadow)

    # Paste the original image on top of the shadow
    original_position = (blur_radius * 2 + max(0, -offset[0])-5, blur_radius * 2 + max(0, -offset[1])-13)
    transparent_canvas.paste(original, original_position, mask=original)

    return transparent_canvas

# Combined function
def process_image_width(image_path, output_path, target_width=1080):
    print("enetering process image" )
    # Step 1: Open the image
    image = Image.open(image_path)
    
    # Step 2: Resize and add borders
    bordered_image = add_borders_and_resize_width(image, target_width=target_width)
    
    # Step 3: Apply drop shadow
    final_image = add_drop_shadow(bordered_image, offset=(10, 20), shadow_color=(0, 0, 0, 150), blur_radius=7)
    
    # Step 4: Save the result
    final_image.save(output_path)
    return final_image

# Combined function
def process_image_height(image_path, output_path, target_height=1080):
    # Open the image with Pillow
    print("enetering process image" )
    image = Image.open(image_path)
    
    # Step 2: Resize and add borders
    bordered_image = add_borders_and_resize_height(image, target_height=target_height)
    
    # Step 3: Apply drop shadow
    final_image = add_drop_shadow(bordered_image, offset=(10, 20), shadow_color=(0, 0, 0, 150), blur_radius=7)
    
    # Step 4: Save the result
    final_image.save(output_path)
    return final_image

def image_transition(image_path, total_duration, clips, new_start_time, pause_duration): 
    image = Image.open(image_path)
    image_width, image_height = image.size
    print("entering image transition")
    if image_height > image_width:
        process_image_height(image_path, "final_output.png", target_height=850)
        image_clip = ImageClip("final_output.png")
        start_position = ("center", (h /2)-300)
        center_position = ("center", abs((h / 2) - (image_clip.h / 2)))
    else:
        
        process_image_width(image_path, "final_output.png", target_width=1080)
        image_clip = ImageClip("final_output.png")
        start_position = ("center", (h /2)-100)
        center_position = ("center", abs((h / 2) - (image_clip.h / 2)))
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    
    # Bind the current iteration's variables
    animated_image = (
        image_clip
        .with_position(lambda t, sp=start_position, cp=center_position,
                       time_to_ctr=time_to_center, pause_dur=pause_duration
                         : move_image(t, sp, cp, time_to_ctr, pause_dur))
        .with_start(new_start_time)
        .with_duration(pause_duration)
    )
    animated_image = animated_image.with_effects([vfx.CrossFadeIn(0.2)])
    clips.append(animated_image)
    total_duration += animated_image.duration
    return total_duration, clips

def video_transition(video_path, total_duration, clips, new_start_time, audio, audio_clips):
    video_clip = VideoFileClip(video_path)
    pause_duration = video_clip.duration
    # audio clips
    if not audio:
        video_clip = video_clip.without_audio()
    else:
        audio_clip = (new_start_time, new_start_time+pause_duration)
        audio_clips.append(audio_clip)
    # Extract the first frame
    frame_width, frame_height = video_clip.w, video_clip.h
    
    if frame_height > frame_width:
        video_clip = video_clip.resized(height=850)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("final_output.png")
        frame_image = "final_output.png"
        process_image_height(frame_image, "final_output.png", target_height=850)
        frame_image = ImageClip("final_output.png")
        start_position = (721, (h /2)-300)
        shadow_position = (721-21, start_position[1]-12)
        shadow_center = (721-21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = (721, abs((h / 2) - (frame_image.h / 2)))
    else:
        video_clip = video_clip.resized(width=1080)
        frame_width, frame_height = video_clip.w, video_clip.h
        frame_image = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
        frame_image.save("final_output.png")
        frame_image = "final_output.png"
        process_image_width(frame_image, "final_output.png", target_width=1080)
        frame_image = ImageClip("final_output.png")
        start_position = ("center", (h /2)-100)
        shadow_position = (420-21, start_position[1]-12)
        shadow_center = (420 -21, abs((h / 2) - (frame_image.h / 2))-13)
        center_position = ("center", abs((h / 2) - (frame_image.h / 2)))
    distance_to_center = start_position[1] - center_position[1]
    time_to_center = distance_to_center / speed
    
    # animating shadow
    shadow = ImageClip("final_output.png")
    animated_shadow = (
    shadow 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=shadow_position, cp=shadow_center,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_image(t, sp, cp, time_to_ctr, pause_dur))
    )
    animated_shadow = animated_shadow.with_effects([vfx.CrossFadeIn(0.2)])
    animated_video = (
    video_clip 
    .with_start(new_start_time)
    .with_duration(pause_duration)
    .with_position(lambda t, sp=start_position, cp=center_position,
                   time_to_ctr=time_to_center, pause_dur=pause_duration:
                   move_image(t, sp, cp, time_to_ctr, pause_dur))

    )
    animated_video = animated_video.with_effects([vfx.CrossFadeIn(0.2)])
    clips.append(animated_shadow)
    clips.append(animated_video)
    print(animated_video.duration)
    total_duration += animated_video.duration
    return total_duration, clips, audio_clips

def adding_background_audio(audio_clips1, audio_clips2, volume_audio):
    audio_clips = []
    previous_end = (0, 0)
    print("entering add_background_audio for clip1")
    for audio_clip in audio_clips1:
        segment = volume_audio.subclipped(previous_end[1], audio_clip[0]).with_effects([afx.AudioFadeOut("00:00:01"), afx.AudioFadeIn("00:00:01")])
        audio_clips.append(segment)
        silence_duration = audio_clip[1] - audio_clip[0]
        silence_clip = AudioClip(lambda t: 0, duration=silence_duration)
        audio_clips.append(silence_clip)
        previous_end = audio_clip


    resume_segment = volume_audio.subclipped(previous_end[0], volume_audio.duration).with_effects([afx.AudioFadeIn("00:00:01")])
    audio_clips.append(resume_segment)
    print("entering add_background_audio for clip2")
    if audio_clips2 != []:
        audio_clips = audio_clips[:-1]
        duration = float(video1.duration + intro_video.duration)
        for audio_clip in audio_clips2:
            start_time = float(audio_clip[0] + duration)
            end_time = float(audio_clip[1] + duration)
            segment = volume_audio.subclipped(previous_end[1], start_time).with_effects([afx.AudioFadeOut("00:00:01"), afx.AudioFadeIn("00:00:01")])
            audio_clips.append(segment)
            silence_duration = end_time - start_time
            silence_clip = AudioClip(lambda t: 0, duration=silence_duration)
            audio_clips.append(silence_clip)    
            previous_end = (start_time, end_time)

        resume_segment = volume_audio.subclipped(start_time, volume_audio.duration).with_effects([afx.AudioFadeIn("00:00:01")])
        audio_clips.append(resume_segment)
    print("concatenating audios...")
    Final_background_audio = concatenate_audioclips(audio_clips)
    Final_background_audio = Final_background_audio.subclipped(0,final_with_outro.duration)
    volume_audio = Final_background_audio.with_effects([afx.AudioFadeOut("00:00:04")])
    return volume_audio

def adding_transcripts_audio(transcript_audio):
    audio_list = []
    print("adding transcript audio ....")
    for item in transcript_audio:
        url = item["url"]
        start_time = item["start_time"]
        audio = AudioFileClip(url)
        clip = audio.with_start(start_time)
        audio_list.append(clip) 
    combined_intro_audio = CompositeAudioClip(audio_list)
    return combined_intro_audio

background_video = VideoFileClip('BG Template.mp4')
background_audio = AudioFileClip('music.mp3')
intro_video = VideoFileClip('intro.mp4')
outro_video = VideoFileClip('outro.mp4')
w, h = background_video.size
audio_clips1 = []
audio_clips2 = []
speed = 800 
transcript_audio =  [
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-0-1733649403232.mp3", "start_time": 0},
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-1-1733649404581.mp3", "start_time": 7},
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-2-1733649403481.mp3", "start_time": 55},
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S3-1733649377342.mp3", "start_time": 62},
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S4-1733649383601.mp3", "start_time": 80},
    {"url": "https://machine-genius.s3.amazonaws.com/My_Audios/audio-S2-1733649377093.mp3", "start_time": 99},
  ]
intro =[
    {"url": "https://dl.claid.ai/33376023-a6d7-4889-abe7-218af50c1914/1200px-Donald_Trump_official_portrait.jpeg", "pause_duration": 8},
    {"url": "https://cdn.prod.www.spiegel.de/images/e22063c2-3ec7-4749-b56d-f2c7a61501cb_w960_r1.778_fpx51_fpy50.jpg", "pause_duration": 10},
    {"url": "https://machine-genius.s3.us-east-1.amazonaws.com/youtubevideos/0DSxBOkXZyE_1731321496326.mp4", "with_audio": True},
    {"url": "https://dl.claid.ai/7e2fab0e-7fe8-4e10-9b7d-ba0294c1a167/trump-portrait_square.jpeg", "pause_duration": 10},
    {"url": "https://dl.claid.ai/33376023-a6d7-4889-abe7-218af50c1914/1200px-Donald_Trump_official_portrait.jpeg", "pause_duration": 4}
]
clips = []
audio_clips = []
total_duration = 0
audio = True
new_start_time = 0
print("enetering the loop...." )
for item in intro: 
    media_path = item["url"]
    file_extension = os.path.splitext(media_path)[1].lower()
    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', 'webp']:
        pause_duration = item["pause_duration"]
        print("requesting image...")
        response = requests.get(media_path)
        image_data = BytesIO(response.content)
        total_duration, clips = image_transition(image_data, total_duration, clips, new_start_time, pause_duration)
        print("finishing a transition...")
    elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
        audio = item["with_audio"]
        total_duration, clips, audio_clips1 = video_transition(media_path, total_duration, clips, new_start_time, audio, audio_clips)
    print(total_duration)
    new_start_time = total_duration

## modify the duration of background video ##
background_video_repeated = repeat_video(video=background_video, total_duration=total_duration)
logo_image = ImageClip("WATERMARK.png").resized(width=150).with_position((1740,900)).with_duration(background_video_repeated.duration)
clips.append(logo_image)
# audio_track = CompositeAudioClip(audio_clips)
video = CompositeVideoClip([background_video_repeated] + clips)
video.write_videofile("video1.mp4", fps=30)
#######################################1
content =[
    {"url": "https://dl.claid.ai/33376023-a6d7-4889-abe7-218af50c1914/1200px-Donald_Trump_official_portrait.jpeg", "pause_duration": 10},
    {"url": "https://cdn.prod.www.spiegel.de/images/e22063c2-3ec7-4749-b56d-f2c7a61501cb_w960_r1.778_fpx51_fpy50.jpg", "pause_duration": 5},
    {"url": "https://dl.claid.ai/7e2fab0e-7fe8-4e10-9b7d-ba0294c1a167/trump-portrait_square.jpeg", "pause_duration": 5},
    {"url": "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iYajQbcnQB04/v1/-1x-1.webp", "pause_duration": 6}
]
clips = []
total_duration = 0
audio_clips = []
audio = True
new_start_time = 0

for item in content:
    media_path = item["url"]
    file_extension = os.path.splitext(media_path)[1].lower()
    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
        pause_duration = item["pause_duration"]
        print("requesting image...")
        response = requests.get(media_path)
        image_data = BytesIO(response.content)
        total_duration, clips = image_transition(image_data, total_duration, clips, new_start_time, pause_duration)
    elif file_extension in ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']:
       audio = item["with_audio"]
       total_duration, clips, audio_clips2 = video_transition(media_path, total_duration, clips, new_start_time, audio, audio_clips)
    new_start_time = total_duration

## modify the duration of background video ##
background_video_repeated = repeat_video(video=background_video,total_duration=total_duration)
logo_image = ImageClip("WATERMARK.png").resized(width=150).with_position((1740,900)).with_duration(background_video_repeated.duration)
clips.append(logo_image)
video = CompositeVideoClip([background_video_repeated] + clips)
video.write_videofile("video2.mp4", fps=30)
#####################################
video1 = VideoFileClip("video1.mp4")
video2 = VideoFileClip("video2.mp4")
final_video = concatenate_videoclips([video1, intro_video, video2])
final_with_outro = CompositeVideoClip([final_video, outro_video.with_effects([vfx.SlideIn(0.3, "top")]).with_start(final_video.duration - 1)]).subclipped()
background_audio = background_audio.subclipped(0,final_with_outro.duration)

background_audio = adding_background_audio(audio_clips1, audio_clips2, background_audio)

transcript_audio = adding_transcripts_audio(transcript_audio)
combined_audio = CompositeAudioClip([transcript_audio, final_video.audio, background_audio])
final = final_with_outro.with_audio(combined_audio)
final.write_videofile("output1.mp4", fps=30)
