from .Main import create_video
from celery import shared_task

@shared_task
def create_video_task(intro, transcript_audio, content):
    path = create_video( intro, transcript_audio, content)
    print(path)