from moviepy import *
import requests
def adding_transcripts_audio(transcript_audio):
    audio_list = []
    for item in transcript_audio:
        url = item["url"]
        start_time = item["start_time"]
        local_filename = "downloads/sample.mp3"

# Perform the GET request and download the file
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  
                    file.write(chunk)
        audio = AudioFileClip(local_filename)
        clip = audio.with_start(start_time)
        audio_list.append(clip) 
    combined_intro_audio = CompositeAudioClip(audio_list)
    return combined_intro_audio