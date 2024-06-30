from api import bp
from api import redishelper
from api import constants
from api import utils
from http import HTTPStatus
import datetime
from flask import request, render_template, url_for, jsonify
import json
import logging


@bp.route("/")
@redishelper.redis_connection
def landscreen():
    try:
        err, keys = redishelper.get_all_keys()
        if err:
            return render_template("home.jinja2", elements=[]), HTTPStatus.INTERNAL_SERVER_ERROR
        values = []
        for key in keys:
            err, val = redishelper.get_key(key=key)
            if err:
                break
            val = json.loads(val)
            val["alias"] = key.decode('ascii')
            print(val)
            values.append(val)
        return render_template("home.jinja2", elements=values), HTTPStatus.OK
    except Exception as e:
        logging.critical(f"Couldn't initialize landscreen due to {str(e)}")
        return render_template("home.jinja2", elements=[]), HTTPStatus.OK

@bp.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.ico'), HTTPStatus.OK

@bp.route("/<id>", methods=['GET'])
@bp.route("/<id>/", methods=['GET'])
@redishelper.redis_connection
def get_link(id):
    return utils.link_details(id, describe=False), HTTPStatus.PERMANENT_REDIRECT

@bp.route("/describe/<id>", methods=['GET'])
@bp.route("/describe/<id>/", methods=['GET'])
@redishelper.redis_connection
def describe_link(id):
    return utils.link_details(id, describe=True), HTTPStatus.OK

@bp.route("/delete/<id>", methods=['DELETE'])
@bp.route("/delete/<id>/", methods=['DELETE'])
@redishelper.redis_connection
def delete_alias(id):
    err, found = redishelper.get_key(id)
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    if found is None:
        return utils.paragraph_tag("Not Found"), HTTPStatus.NOT_FOUND
    err, res = redishelper.delete_key(id)
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    return utils.paragraph_tag("Done"), HTTPStatus.OK

@bp.route("/add", methods=['POST'])
@bp.route("/add/", methods=['POST'])
@redishelper.redis_connection
def add_link():
    err = utils.request_validator(request)
    if err:
        return err, HTTPStatus.BAD_REQUEST
    link = request.form.get(constants.URL_PARAMS_LINK)
    alias = request.form.get(constants.URL_PARAMS_ALIAS)
    err, duplicate = redishelper.get_key(alias)
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    if duplicate is not None:
        return utils.paragraph_tag("Duplicate alias"), HTTPStatus.BAD_REQUEST
    data = {
        constants.URL_PARAMS_LINK : link,
        constants.URL_PARAMS_CREATED: str(datetime.datetime.now())
        }
    owner = request.form.get(constants.URL_PARAMS_OWNER)
    if owner:
        data[constants.URL_PARAMS_OWNER] = owner
    category = request.form.get(constants.URL_PARAMS_CATEGORY)
    if category:
        data[constants.URL_PARAMS_CATEGORY] = category
    site = request.form.get(constants.URL_PARAMS_SITE)
    if site:
        data[constants.URL_PARAMS_SITE] = site
    err, resp = redishelper.set_key(alias, json.dumps(data))
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    return utils.paragraph_tag("Done"), HTTPStatus.OK

@bp.route("/replace", methods=['POST'])
@bp.route("/replace/", methods=['POST'])
@redishelper.redis_connection
def replace_link():
    err = utils.request_validator(request)
    if err:
        return err, HTTPStatus.BAD_REQUEST
    link = request.form.get(constants.URL_PARAMS_LINK)
    alias = request.form.get(constants.URL_PARAMS_ALIAS)
    err, current_data = redishelper.get_key(alias)
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    data = {
        constants.URL_PARAMS_LINK : link,
        }
    if current_data is not None:
        data[constants.URL_PARAMS_MODIFIED] = str(datetime.datetime.now())
        current_data = json.loads(current_data)
        if current_data.get(constants.URL_PARAMS_CREATED):
            data[constants.URL_PARAMS_CREATED] = current_data.get(constants.URL_PARAMS_CREATED)
        else:
            data[constants.URL_PARAMS_CREATED] = str(datetime.datetime.now())
        if current_data.get(constants.URL_PARAMS_OWNER):
            data[constants.URL_PARAMS_OWNER] = current_data.get(constants.URL_PARAMS_OWNER)
        if current_data.get(constants.URL_PARAMS_CATEGORY):
            data[constants.URL_PARAMS_CATEGORY] = current_data.get(constants.URL_PARAMS_CATEGORY)
        if current_data.get(constants.URL_PARAMS_SITE):
            data[constants.URL_PARAMS_SITE] = current_data.get(constants.URL_PARAMS_SITE)
    else:
        data[constants.URL_PARAMS_CREATED] = str(datetime.datetime.now())
    owner = request.form.get(constants.URL_PARAMS_OWNER)
    if owner:
        data[constants.URL_PARAMS_OWNER] = owner
    category = request.form.get(constants.URL_PARAMS_CATEGORY)
    if category:
        data[constants.URL_PARAMS_CATEGORY] = category
    err, resp = redishelper.set_key(alias, json.dumps(data))
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    return utils.paragraph_tag("Done"), HTTPStatus.OK

@bp.route("/edit", methods=['POST'])
@bp.route("/edit/", methods=['POST'])
@redishelper.redis_connection
def edit():
    err = utils.request_edit_validator(request)
    if err:
        return err, HTTPStatus.BAD_REQUEST
    link = request.form.get(constants.URL_PARAMS_LINK)
    old_alias = request.form.get(constants.URL_PARAMS_EDIT_OLD_ALIAS)
    new_alias = request.form.get(constants.URL_PARAMS_EDIT_NEW_ALIAS)

    if old_alias != new_alias:
        err, duplicate = redishelper.get_key(new_alias)
        if err:
            return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
        if duplicate is not None:
            return utils.paragraph_tag("Duplicate alias"), HTTPStatus.BAD_REQUEST
    
    err, current_data = redishelper.get_key(old_alias)
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    data = {
        constants.URL_PARAMS_LINK : link,
        constants.URL_PARAMS_CREATED: str(datetime.datetime.now())
        }
    
    if current_data is not None:
        data[constants.URL_PARAMS_MODIFIED] = str(datetime.datetime.now())
        current_data = json.loads(current_data)
        if current_data.get(constants.URL_PARAMS_CREATED):
            data[constants.URL_PARAMS_CREATED] = current_data.get(constants.URL_PARAMS_CREATED)

        # Delete Key
        err, res = redishelper.delete_key(old_alias)
        if err:
            return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    
    owner = request.form.get(constants.URL_PARAMS_OWNER)
    if owner:
        data[constants.URL_PARAMS_OWNER] = owner
    category = request.form.get(constants.URL_PARAMS_CATEGORY)
    if category:
        data[constants.URL_PARAMS_CATEGORY] = category
    site = request.form.get(constants.URL_PARAMS_SITE)
    if site:
        data[constants.URL_PARAMS_SITE] = site
    err, resp = redishelper.set_key(new_alias, json.dumps(data))
    if err:
        return utils.paragraph_tag(err), HTTPStatus.INTERNAL_SERVER_ERROR
    return utils.paragraph_tag("Done"), HTTPStatus.OK

