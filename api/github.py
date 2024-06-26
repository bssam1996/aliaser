import requests
import base64
import json
import datetime
import logging


def push_to_repo_branch(gitHubFileName, fileName, repo_slug, branch, user, token):
    '''
    Push file update to GitHub repo
    
    :param gitHubFileName: the name of the file in the repo
    :param fileName: the name of the file on the local branch
    :param repo_slug: the github repo slug, i.e. username/repo
    :param branch: the name of the branch to push the file to
    :param user: github username
    :param token: github user token
    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    '''
    
    message = "Automated update " + str(datetime.datetime.now())
    path = f"https://api.github.com/repos/{repo_slug}/branches/{branch}"

    r = requests.get(path, auth=(user,token))
    if not r.ok:
        logging.critical(f"Error when retrieving branch info from {path}")
        logging.critical(f"Reason: {r.text} [{r.status_code}]")
        return False
    rjson = r.json()
    treeurl = rjson['commit']['commit']['tree']['url']
    r2 = requests.get(treeurl, auth=(user,token))
    if not r2.ok:
        logging.critical(f"Error when retrieving commit tree from {treeurl}")
        logging.critical(f"Reason: {r2.text} [{r2.status_code}]")
        return False
    r2json = r2.json()
    sha = None

    for file in r2json['tree']:
        # Found file, get the sha code
        if file['path'] == gitHubFileName:
            sha = file['sha']

    # if sha is None after the for loop, we did not find the file name!
    if sha is None:
        logging.critical("Could not find " + gitHubFileName + " in repos 'tree' ")
        return False

    with open(fileName) as data:
        content = base64.b64encode(data.read().encode("utf-8"))

    # gathered all the data, now let's push
    inputdata = {}
    inputdata["path"] = gitHubFileName
    inputdata["branch"] = branch
    inputdata["message"] = message
    inputdata["content"] = content.decode()
    if sha:
        inputdata["sha"] = str(sha)

    updateURL = f"https://api.github.com/repos/{repo_slug}/contents/" + gitHubFileName
    try:
        rPut = requests.put(updateURL, auth=(user,token), data = json.dumps(inputdata))
        if not rPut.ok:
            logging.critical("Error when pushing to %s" % updateURL)
            logging.critical("Reason: %s [%d]" % (rPut.text, rPut.status_code))
            return False
    except requests.exceptions.RequestException as e:
        logging.critical('Something went wrong! I will print all the information that is available so you can figure out what happend!')
        logging.critical(rPut)
        logging.critical(rPut.headers)
        logging.critical(rPut.text)
        logging.critical(e)
        return False
    return True