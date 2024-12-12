from moviepy import *
def adding_background_audio(video1, intro_video, final_with_outro, audio_clips1, audio_clips2, volume_audio):
    audio_clips = []
    previous_end = (0, 0)
    for audio_clip in audio_clips1:
        segment = volume_audio.subclipped(previous_end[1], audio_clip[0]).with_effects([afx.AudioFadeOut("00:00:01"), afx.AudioFadeIn("00:00:01")])
        audio_clips.append(segment)
        silence_duration = audio_clip[1] - audio_clip[0]
        silence_clip = AudioClip(lambda t: 0, duration=silence_duration)
        audio_clips.append(silence_clip)
        previous_end = audio_clip


    resume_segment = volume_audio.subclipped(previous_end[0], volume_audio.duration).with_effects([afx.AudioFadeIn("00:00:01")])
    audio_clips.append(resume_segment)
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
    Final_background_audio = concatenate_audioclips(audio_clips)
    Final_background_audio = Final_background_audio.subclipped(0,final_with_outro.duration)
    volume_audio = Final_background_audio.with_effects([afx.AudioFadeOut("00:00:04")])
    return volume_audio