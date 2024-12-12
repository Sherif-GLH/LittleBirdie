from moviepy import *
def adding_transcripts_audio(transcript_audio):
    audio_list = []
    for item in transcript_audio:
        url = item["url"]
        start_time = item["start_time"]
        audio = AudioFileClip(url)
        clip = audio.with_start(start_time)
        audio_list.append(clip) 
    combined_intro_audio = CompositeAudioClip(audio_list)
    return combined_intro_audio