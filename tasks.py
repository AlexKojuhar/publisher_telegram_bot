import schedule
import time
import requests
import os

from db import find_last_unpublish_video, set_video_is_published
from tiktok_uploader.upload import upload_video

url = "https://api.telegram.org/bot{}/sendMessage".format(os.environ.get('BOT_TOKEN'))

def upload_video_to_tiktok():
    try:
        video_to_publish = find_last_unpublish_video()
        print('video_to_publish', video_to_publish)
        if (video_to_publish):
            upload_video(filename=video_to_publish['path'],
                description=video_to_publish['tags'],
                cookies='cookies.txt',
                browser='chrome'
            )
            set_video_is_published(video_to_publish['id'])
            send_message_about_video_publisging_to_telegram(video_to_publish['chat_id'], video_to_publish['message_id'])
            remove_video_after_publishing(video_to_publish['path'])
        else:
            print('All video was already published.')
    except Exception as e:
        print(f"Error upload_video_to_tiktok: {e}")
        return None
    
def remove_video_after_publishing(path):
    if os.path.exists(path):
        os.remove(path)
        print("The file {} was removed".format(path))
    else:
        print("The file {} does not exist".format(path))
    
def send_message_about_video_publisging_to_telegram(chat_id, message_id):
    if (chat_id and message_id):
        payload = {
            "chat_id": chat_id,
            "text": "This video published to TikTok.",
            "disable_web_page_preview": False,
            "disable_notification": False,
            "reply_to_message_id": message_id
        }
        headers = {
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if (response.ok):
            print('Message about publishing is send.')
        else:
            print('send_message_about_video_publisging_to_telegram: Can`t send message to chat_id={} and message_id={}'.format(chat_id, message_id))
        print(response.text)
    

schedule.every().day.at("12:00").do(upload_video_to_tiktok)
schedule.every().day.at("18:00").do(upload_video_to_tiktok)
# schedule.every().minutes.do(upload_video_to_tiktok)

while True:
    schedule.run_pending()
    time.sleep(1)