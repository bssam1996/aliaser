from api import bp
from api import filehelper
from api import git
from api import redishelper
from flask import request, render_template, redirect
import json

@bp.route("/")
@redishelper.redis_connection
def landscreen():
    # if helpers.locations_data is None:
    #     print("Data is empty ... importing data")
    #     helpers.parse_file()
    return render_template("home.jinja2") 

@bp.route("/<id>", methods=['GET'])
@bp.route("/<id>/", methods=['GET'])
@redishelper.redis_connection
def get_link(id):
    print(f"id : {id}")
    err, link = redishelper.get_key(id)
    if err:
        return f"<p>{err}</p>"
    if link:
        link = json.loads(link)
        link = link.get("link")
        return redirect(f"{link}")
    return "<p>Empty</p>"

@bp.route("/describe/<id>", methods=['GET'])
@bp.route("/describe/<id>/", methods=['GET'])
@redishelper.redis_connection
def describe_link(id):
    err, link = redishelper.get_key(id)
    if err:
        return f"<p>{err}</p>"
    if link:
        link = json.loads(link)
        return link
    return "<p>Empty</p>"

@bp.route("/add", methods=['POST'])
@bp.route("/add/", methods=['POST'])
@redishelper.redis_connection
def add_link():
    err = request_validator(request)
    if err:
        return err
    link = request.form.get("link")
    alias = request.form.get("alias")
    err, duplicate = redishelper.get_key(alias)
    if err:
        return f"<p>{err}</p>"
    if duplicate is not None:
        return "<p>Duplicate alias</p>"
    data = {"link" : link}
    err, resp = redishelper.set_key(alias, json.dumps(data))
    if err:
        return f"<p>{err}</p>"
    # git.push_to_repo_branch(helpers.FILE_NAME, helpers.FILE_PATH + helpers.FILE_NAME, "bssam1996/aliaser", "main", "bssam1996", "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")
    return "<p>Done</p>"

@bp.route("/replace", methods=['POST'])
@bp.route("/replace/", methods=['POST'])
@redishelper.redis_connection
def replace_link():
    err = request_validator(request)
    if err:
        return err
    link = request.form.get("link")
    alias = request.form.get("alias")
    data = {"link" : link}
    err, resp = redishelper.set_key(alias, json.dumps(data))
    if err:
        return f"<p>{err}</p>"
    return "<p>Done</p>"


def request_validator(req):
    try:
        if len(request.form) == 0:
            return "<p>Empty data sent</p>"
        if request.form.get("link") is None:
            return "<p>Link doesn't exist</p>"
        if request.form.get("alias") is None:
            return "<p>alias doesn't exist</p>"
        http_string = "http://"
        https_string = "https://"
        link = request.form.get("link")
        if len(link) < len(http_string) or \
                link[:len(http_string)] != http_string and \
                link[:len(https_string)] != https_string:
            return "<p>link must start with http or https</p>"
    except Exception as e:
            print(f"Couldn't parse data due to {str(e)}")
            return "<p>Couldn't parse data</p>"
    return None