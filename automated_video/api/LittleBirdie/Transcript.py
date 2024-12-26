from moviepy import *
import requests, os

def adding_transcripts_audio(transcript_audio):
    audio_list = []
    i = 0
    for item in transcript_audio:
        url = item["url"]
        start_time = item["start_time"]
        local_filename = f"downloads/sample{i}.mp3"

# Perform the GET request and download the file
        response = requests.get(url, stream=True) 
        response.raise_for_status()  
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)
        audio = AudioFileClip(local_filename)
        clip = audio.with_start(start_time)
        audio_list.append(clip)
        remove_local_file(local_filename) 
        i += 1
    combined_intro_audio = CompositeAudioClip(audio_list)
    return combined_intro_audio

def remove_local_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed local file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")