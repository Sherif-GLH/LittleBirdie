from .LittleBirdie.Main import create_video
from celery import shared_task
import requests, subprocess
from django.conf import settings
from celery.app.control import Inspect

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
    check_tasks()

def shutdown_instance():
     subprocess.run(["sudo", "shutdown", "-h", "now"])

def check_tasks():
   active = Inspect.active()
   reserved = Inspect.reserved()
   scheduled = Inspect.scheduled()


   if not any(active.values()) and not any(reserved.values()) and not any(scheduled.values()):
     print("No tasks found in the queue...... shutting the instance down")
     shutdown_instance()

