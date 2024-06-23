import gitlab
import base64
import os
import gitlab.exceptions
import logging
import datetime
from api import filehelper

gl = None

def gitlab_auth():
    global gl
    gitlab_token = os.getenv("GITLAB_PROJECT_TOKEN")
    if gitlab_token is None or gitlab_token == "":
        logging.critical("GITLAB_PROJECT_TOKEN is not set")
        return "GITLAB_PROJECT_TOKEN is not set"
    gitlab_link = os.getenv("GITLAB_HOST")
    if gitlab_link is None or gitlab_link == "":
        logging.warn("GITLAB_HOST is not set, using http://localhost:80 instead")
        gitlab_link = "http://localhost:80"
    try:
        gl = gitlab.Gitlab(gitlab_link, private_token=gitlab_token, ssl_verify='/etc/ssl/cert.pem')
        gl.auth()
        return None
    except Exception as e:
        logging.critical(f"Error while trying to connect to gitlab: {str(e)}")
        gl = None
        return str(e)

def get_file_content():
    # get the file object
    try:
        project_id, project_branch, err = validate_params()
        if err:
            return err, None
        global gl
        if gl is None:
            err = gitlab_auth()
            if err:
                return err, None
        project = gl.projects.get(project_id) # Id of the project
        f = project.files.get(file_path=filehelper.FILE_NAME, ref=project_branch)
        content = base64.b64decode(f.content)
        return None, content.decode('utf-8')
    except gitlab.exceptions.GitlabGetError as e:
        if str(e).count('404') > 0:
            print('Not Found')
            return None, None
        return str(e), None

def modify_content():
    try:
        project_id, project_branch, err = validate_params()
        if err:
            return err
        global gl
        if gl is None:
            err = gitlab_auth()
            if err:
                return err
        project = gl.projects.get(project_id) # Id of the project
        f = project.files.get(file_path=filehelper.FILE_NAME, ref=project_branch)
        with open(filehelper.FILE_PATH + filehelper.FILE_NAME, 'rb') as my_file:
            f.content = base64.b64encode(my_file.read()).decode('utf-8')
        message = "Automated update " + str(datetime.datetime.now())
        f.save(branch=project_branch, commit_message=message, encoding='base64')
        return None
    except gitlab.exceptions.GitlabGetError as e:
        if str(e).count('404') > 0:
            print('Not Found')
            return 'Not Found'
        return str(e)

def create_file():
    try:
        project_id, project_branch, err = validate_params()
        if err:
            return err
        global gl
        if gl is None:
            err = gitlab_auth()
            if err:
                return err
        project = gl.projects.get(project_id) # Id of the project
        with open(filehelper.FILE_PATH + filehelper.FILE_NAME, 'rb') as my_file:
            contents = base64.b64encode(my_file.read()).decode('utf-8')
        # create new file in the repo
        message = "Automated update " + str(datetime.datetime.now())
        f = project.files.create({'file_path': filehelper.FILE_NAME,
                                'branch': project_branch,
                                'content': contents,
                                'encoding': 'base64',
                                'author_email': 'aliaser@cgg.com',
                                'author_name': 'aliaser',
                                'commit_message': message})
        return None
    except Exception as e:
        logging.critical(f"Couldn't create file due to {str(e)}")
        return str(e)
    
def validate_params():
    project_id = os.getenv("GITLAB_PROJECT_ID")
    if project_id is None or project_id == "":
        logging.critical("GITLAB_PROJECT_ID is not set")
        return None, None, "GITLAB_PROJECT_ID is not set"
    if not project_id.isnumeric():
        logging.critical("GITLAB_PROJECT_ID is not numeric")
        return None, None, "GITLAB_PROJECT_ID is not numeric"
    project_id = int(project_id)
    project_branch = os.getenv("GITLAB_PROJECT_BRANCH")
    if project_branch is None or project_branch == "":
        logging.warn("GITLAB_PROJECT_BRANCH is not set, using main")
        project_branch = 'main'
    return project_id, project_branch, None