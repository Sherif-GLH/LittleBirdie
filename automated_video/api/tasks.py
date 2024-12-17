from .Main import create_video
from celery import shared_task
import requests
from django.conf import settings

@shared_task
def create_video_task(intro, transcript_audio, content, video_name, metadata, webhook_url):
    path = create_video(intro, transcript_audio, content, video_name)
    url =  settings.MEDIA_URL + path
    payload = {
        "url": url,
        "metadata" : metadata
    }
    try:
        response = requests.post(webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending video notification: {e}")