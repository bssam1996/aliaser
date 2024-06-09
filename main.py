from flask import Flask
import os
import time
from dotenv import load_dotenv
import threading
from api import redishelper
from api import filehelper
from api import git
import json

app = Flask(__name__, template_folder="templates")

load_dotenv()

from api import bp as main_bp
app.register_blueprint(main_bp)

def main():
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    debug = os.getenv('DEBUG')

    # Init Redis
    init_redis_thread = threading.Thread(target=init_redis, daemon=True)
    init_redis_thread.start()

    # Backup to git
    backup_thread = threading.Thread(target=backup_to_git, daemon=True)
    backup_thread.start()

    app.run(host=host, port=port, debug=debug, use_reloader=False)

def init_redis():
    try:
        while redishelper.REDIS_CLIENT is None:
            print("Connecting to redis from init thread")
            redishelper.connect_to_redis()
            time.sleep(1)
        err, num_of_keys = redishelper.get_length_keys()
        if err:
            print(err)
            return
        if num_of_keys != 0:
            print(f"Redis has keys with length {str(num_of_keys)}")
            return
        # Parse the file
        filehelper.parse_file()
        # Push the data into redis
        if filehelper.locations_data is None:
            print("Empty data in git")
            return
        for key in filehelper.locations_data:
            data = filehelper.locations_data.get(key)
            redishelper.set_key(key, json.dumps(data))
    except Exception as e:
        print(f"Error in thread: {str(e)}")
    
def backup_to_git():
    schedule_time = os.getenv('BACKUP_SCHEDULE', 3600)
    while True:
        try:
            time.sleep(int(schedule_time)) # 5 minutes
            print("================ Backup Thread started ================")
            while redishelper.REDIS_CLIENT is None:
                print("Connecting to redis from Backup thread")
                redishelper.connect_to_redis()
                time.sleep(1)
            err, keys = redishelper.get_all_keys()
            if err:
                print(err)
                continue
            if len(keys) == 0:
                print(f"Redis has keys with length 0")
                continue
            data = {}
            failed = False
            for key in keys:
                err, val = redishelper.get_key(key)
                if err:
                    print(f"Couldn't get value for {key}")
                    failed = True
                    break
                data[key.decode('ascii')] = json.loads(val)
            if failed:
                continue
            res = filehelper.write_to_file(json.dumps(data), "w")
            if not res:
                print("Failed to backup")
                continue
            # Push to github
            print("================ Backup Thread pushing to repo ================")
            res = git.push_to_repo_branch(filehelper.FILE_NAME, filehelper.FILE_PATH + filehelper.FILE_NAME, "bssam1996/aliaser", "main", "bssam1996", "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")
            if not res:
                print("Failed to backup")
                continue
            print("================ Backup Thread Done ================")
        except Exception as e:
            print(f"Failed in backup thread due to {str(e)}")


if __name__ == "__main__":
    main()