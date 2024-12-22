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
    try:
        check_tasks()
    except Exception as e:
        print(f"An error occurred while checking tasks: {e}")

def shutdown_instance():
     subprocess.run(["sudo", "shutdown", "-h", "now"]) 

def check_tasks():
   try:
    inspect_instance = Inspect()
    active = inspect_instance.active()
    reserved = inspect_instance.reserved()
    scheduled = inspect_instance.scheduled()
   except Exception as e:
      print(e)

   if active == None and scheduled == None and reserved == None:
     print("No tasks found in the queue...... shutting the instance down")
     shutdown_instance()

