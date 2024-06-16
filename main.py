from flask import Flask, render_template
import os
import time
from dotenv import load_dotenv
import threading
from api import redishelper
from api import filehelper
from api import github
from api import gitlabhelper
import json
import logging
from waitress import serve

app = Flask(__name__, template_folder="templates")

load_dotenv()

from api import bp as main_bp
app.register_blueprint(main_bp)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def main():
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 5000)
    debug = os.getenv('DEBUG', True)
    if debug == 'False':
        debug = False
    else:
        debug = True

    logging.basicConfig(level=logging.DEBUG)

    # Init Redis
    init_redis_thread = threading.Thread(target=init_redis, daemon=True)
    init_redis_thread.start()

    # Backup to git
    backup_thread = threading.Thread(target=backup_to_git, daemon=True)
    backup_thread.start()

    if debug:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    else:
        serve(app=app, host=host, port=port)

def init_redis():
    try:
        while redishelper.REDIS_CLIENT is None:
            logging.info("Connecting to redis from init thread")
            redishelper.connect_to_redis()
            time.sleep(1)
        err, num_of_keys = redishelper.get_length_keys()
        if err:
            logging.critical(err)
            return
        if num_of_keys != 0:
            logging.info(f"Redis has keys with length {str(num_of_keys)}")
            return
        # Parse the file
        filehelper.parse_file()
        # Push the data into redis
        if filehelper.locations_data is None:
            logging.info("Empty data in git")
            return
        for key in filehelper.locations_data:
            data = filehelper.locations_data.get(key)
            redishelper.set_key(key, json.dumps(data))
    except Exception as e:
        logging.critical(f"Error in thread: {str(e)}")
    
def backup_to_git():
    schedule_time = os.getenv('BACKUP_SCHEDULE', 3600)
    if schedule_time is None or schedule_time == '':
        schedule_time = 3600
    logging.info(f"Backup thread is set to {schedule_time} seconds")
    while True:
        try:
            time.sleep(int(schedule_time)) # 5 minutes
            logging.info("================ Backup Thread started ================")
            while redishelper.REDIS_CLIENT is None:
                logging.info("Connecting to redis from Backup thread")
                redishelper.connect_to_redis()
                time.sleep(1)
            err, keys = redishelper.get_all_keys()
            if err:
                logging.critical(err)
                continue
            if len(keys) == 0:
                logging.info(f"Redis has keys with length 0")
                continue
            data = {}
            failed = False
            for key in keys:
                err, val = redishelper.get_key(key)
                if err:
                    logging.critical(f"Couldn't get value for {key}")
                    failed = True
                    break
                data[key.decode('ascii')] = json.loads(val)
            if failed:
                continue
            res = filehelper.write_to_file(json.dumps(data), "w")
            if not res:
                logging.critical("Failed to backup")
                continue
            # Push to github
            logging.info("================ Backup Thread pushing to repo ================")
            git_type = os.getenv('GIT_MODE', 'GITLAB')
            if git_type == "" or git_type == "GITLAB":
                logging.info("Gitlab type is specified")
                err = gitlabhelper.modify_content()
                if err and err == 'Not Found':
                    logging.warn("File was not found on the server ... attempting to create it...")
                    err = gitlabhelper.create_file()
                    if err:
                        logging.critical(f"Failed to backup, couldn't create file in gitlab due to {str(e)}")
                        continue
                elif err:
                    logging.critical(f"Failed to backup, couldn't modify file in gitlab due to {str(e)}")
                    continue
            else:
                logging.info("github type is specified")
                repo = os.getenv('GITHUB_REPO')
                branch = os.getenv('GITHUB_BRANCH')
                user = os.getenv('GITHUB_USER')
                token = os.getenv('GITHUB_TOKEN')
                if repo is None or repo == "":
                    logging.critical("Failed to backup as GITHUB_REPO is missing")
                    break
                if branch is None or branch == "":
                    logging.critical("Failed to backup as GITHUB_BRANCH is missing")
                    break
                if user is None or user == "":
                    logging.critical("Failed to backup as GITHUB_USER is missing")
                    break
                if token is None or token == "":
                    logging.critical("Failed to backup as GITHUB_TOKEN is missing")
                    break
                res = github.push_to_repo_branch(filehelper.FILE_NAME, filehelper.FILE_PATH + filehelper.FILE_NAME, repo, branch, user, token)
            if not res:
                logging.critical("Failed to backup")
                continue
            logging.info("================ Backup Thread Done ================")
        except Exception as e:
            logging.critical(f"Failed in backup thread due to {str(e)}")


if __name__ == "__main__":
    main()