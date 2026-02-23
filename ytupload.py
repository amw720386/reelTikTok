import os
import pickle
from os import listdir, remove, path

import google.auth.transport.requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from datetime import datetime, timedelta, timezone

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE =  os.getenv("client_secret_file")
TOKEN_FILE = os.getenv("token_file")

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_video(file_path, title, description, tags, category_id=22, delay_hours=3):
    youtube = get_authenticated_service()

    publish_time = datetime.now(timezone.utc) + timedelta(hours=delay_hours)
    publish_at_str = publish_time.isoformat()

    request_body = {
        'snippet': {
            'title': title[:100],
            'description': description,
            'tags': tags,
            'categoryId': category_id,
            'scheduledPublishTime': publish_at_str 
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_at_str,
            'madeForKids': False
        }
    }

    try:
        with open(file_path, 'rb') as video_file:
            request = youtube.videos().insert(
                part="snippet,status",
                body=request_body,
                media_body=MediaIoBaseUpload(video_file, mimetype='video/*')
            )
            response = request.execute()
            print(f"Video scheduled for {publish_at_str} (UTC): https://youtu.be/{response['id']}")
    except HttpError as e:
        print(f"An error occurred: {e}")

def deleteFiles(directory, extension=""):
    for f in listdir(directory):
        if extension == "" or f.endswith(extension):
            try:
                remove(path.join(directory, f))
            except Exception as e:
                print(f"⚠️ Error deleting {f}: {e}")

file_path = 'data/output/final.mp4'
with open("data/title.txt", "r") as f:
    title = f.readline().strip()
description = f'{title} ❤️ 😯 #shorts #Shorts #reddit #askreddit #redditquestions #fyp #fypage'
tags = ['reddit', 'askreddit', 'redditquestions', 'shorts', 'Shorts', "funny stories", "viral", 'fyp', 'fypage']

upload_video(file_path, title, description, tags)

deleteFiles("./data/audio", ".mp3")
deleteFiles("./data/screenshots", ".png")
deleteFiles("./data/cache", ".avi")
deleteFiles("./data/cache", ".mp3")
deleteFiles("./data", ".txt")
