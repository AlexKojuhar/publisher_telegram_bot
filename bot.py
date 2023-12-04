import telebot
import os
import re
from dotenv import load_dotenv
from instagrapi import Client
from db import add_video_to_db, check_if_video_already_exist, check_if_user_can_publish, get_unpublished_videos
from helpers import create_dir_if_not_exist

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

cl = Client()
cl.login(os.environ.get('INSTAGRAM_USERNAME'), os.environ.get('INSTAGRAM_PASSWORD'))

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Hello! Send me an Instagram post link, and I will try to download the video for you.")

@bot.message_handler(commands=['list'])
def handle_start_help(message):
    unpublished_videos = get_unpublished_videos()
    if (unpublished_videos):
        videos_string = "\n".join([f"{i + 1}. {video['post_link']}" for i, video in enumerate(unpublished_videos)])
        bot.send_message(message.chat.id, videos_string, parse_mode='markdown')
    else:
        bot.send_message(message.chat.id, 'All video was publish! It`ll be great if you send smth new!')

@bot.message_handler(regexp= r'https?://(www\.)?instagram\.com/[a-zA-Z0-9_]+/?')
def handle_download_video(message):
    post_link = message.text.split()[-1]
    
    if (not is_user_can_publish(message.from_user.id)):
        bot.send_message(message.chat.id, "Sorry, You couldn't post video due to restrictions.")
        return
    
    if (is_video_already_exist(post_link)):
        bot.send_message(message.chat.id, "This video is already uploaded")
        return

    video = download_instagram_video_with_tags(post_link)
    
    if (video):
        add_video_to_db(video['path'], message.from_user.id, message.chat.id, message.message_id ,post_link, video['tags'])
        bot.send_video(message.chat.id, video=open(video['path'], 'rb'), caption=video_message_html(video['tags']), reply_to_message_id=message.id, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't find the video. Make sure the link is for a public Instagram post.")
        
@bot.message_handler(content_types='text')
def handle_response(message):
    bot.send_message(message.chat.id, 'My response to: ' + str(message.chat.id) + ' ' + message.text)

def download_instagram_video_with_tags(post_link):
    try:
        create_dir_if_not_exist('videos')
        media_pk = cl.media_pk_from_url(post_link)
        path = cl.video_download(media_pk, 'videos')
        tags = get_video_tags(media_pk)
        return {
            'path':  os.path.relpath(path),
            'tags': tags
        }
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def video_message_html(caption):
    return caption
    
def get_video_tags(media_pk):
    try:
        media_info = cl.media_info(media_pk).dict()
        media_caption = media_info['caption_text']
        tags = re.findall(r"#(\w+)", media_caption)
        tags_str = ' '.join(map( lambda tag: '#' + tag , tags))

        return tags_str
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def is_video_already_exist(post_link):
    return check_if_video_already_exist(post_link)

def is_user_can_publish(user_id):
    return check_if_user_can_publish(user_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
