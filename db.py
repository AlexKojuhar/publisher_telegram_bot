import sqlite3
from datetime import datetime, timedelta

from helpers import dict_factory, extract_filename_from_path

ONE_DAY_IN_UNIX = 86400
MAX_DAY_COUNT_FOR_SCHEDULING_IN_UNIX = 10 * ONE_DAY_IN_UNIX

def get_unpublished_videos():
    try:
        connection = sqlite3.connect('autouploader.db')

        connection.row_factory = dict_factory   
        cursor = connection.cursor() 
        
        is_published = int(False) 
        
        cursor.execute("SELECT * FROM videos WHERE is_published = ?", (str(is_published),))   
        
        videos = cursor.fetchall()
        print(videos)
        return videos
    
    except sqlite3.Error as error:
        print("get_unpublish_videos: ", error)
        return None
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

def check_if_video_already_exist(post_link):
    try:
        connection = sqlite3.connect('autouploader.db')

        cursor = connection.cursor()     
        
        cursor.execute("SELECT * FROM videos WHERE post_link = ?", (post_link,))   
        
        is_video_exist = bool(cursor.fetchone())
        
        connection.close()
        
        return is_video_exist
    
    except sqlite3.Error as error:
        print("check_if_video_already_exist: ", error)
        return None
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")
            
def check_if_user_can_publish(user_id):
    try:
        connection = sqlite3.connect('autouploader.db')

        cursor = connection.cursor()     
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),) )  
        
        is_user_exist = bool(cursor.fetchone())
        
        connection.close()
        
        return is_user_exist
    
    except sqlite3.Error as error:
        print("check_if_user_can_publish: ", error)
        return None
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")
            

def set_video_is_published(id):
    try:
        connection = sqlite3.connect('autouploader.db')
        connection.row_factory = dict_factory
                
        is_published = int(True)
        published_at =  datetime.now().strftime('%x')

        cursor = connection.cursor()        
        cursor.execute("UPDATE videos SET is_published = ?, published_at = ? WHERE id = ?", (str(is_published), published_at, id))
        
        connection.commit()
        
        print("Python Variables inserted successfully into Sqlite3 table")
        connection.close()
    except sqlite3.Error as error:
        print("set_video_is_published: Failed to insert Python variable into sqlite table", error)
        return None
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

def find_last_unpublish_video():
    try:
        connection = sqlite3.connect('autouploader.db')
        connection.row_factory = dict_factory
                
        is_published = int(False)

        cursor = connection.cursor()
                
        cursor.execute("SELECT * FROM videos WHERE is_published = ?", str(is_published))
        
        last_unpublish_video = cursor.fetchone()
        print('last_unpublish_video', last_unpublish_video)
        connection.close()
        
        return last_unpublish_video
    except sqlite3.Error as error:
        print("find_last_unpublish_video: ", error)
        return None
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")

    return

def add_video_to_db(path, user_id, chat_id, message_id, post_link, tags):
    try:
        connection = sqlite3.connect('autouploader.db')
        
        created_at = datetime.now().strftime('%x')
        
        is_published = int(False)
        name = extract_filename_from_path(path)

        cursor = connection.cursor()
        cursor.execute("INSERT INTO videos (path, name, created_at, user_id, chat_id, message_id, post_link, tags, is_published)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (path, name, created_at, user_id, chat_id, message_id, post_link, tags, is_published))
        
        connection.commit()
        print("Python Variables inserted successfully into Sqlite3 table")
        
        connection.close()
    except sqlite3.Error as error:
        print("add_video_to_db: Failed to insert Python variable into sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")