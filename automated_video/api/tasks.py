from .LittleBirdie.Main import create_video
from celery import shared_task
import requests, boto3, redis
from django.conf import settings



@shared_task
def create_video_task(intro, transcript_audio, content, video_name, metadata, webhook_url):
    path = create_video(intro, transcript_audio, content, video_name)
    url =  settings.MEDIA_URL + path
    payload = {
        "url": url,
        "status": "Done",
        "metadata" : metadata
    }
    try:
        response = requests.post(webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending video notification: {e}")
    
    b = is_last_task()
    

def shutdown_instance():
    print("Shutting down the instance...")
    ec2 = boto3.client('ec2', region_name='us-east-1')
    instance_id = 'i-0f027204f2e90802c'  
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is stopping.")

def is_last_task(queue_name='celery', redis_host='redis', redis_port=6379, redis_db=0):
    try:
        # Connect to Redis
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

        # Get the length of the queue
        queue_length = redis_client.llen(queue_name)

        if queue_length == 0:
            print("This is the last task. No tasks are waiting in the queue.")
            shutdown_instance()
            return True

    except Exception as e:
        print(f"Error checking queue length: {e}")
        return None

