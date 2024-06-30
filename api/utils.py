from api import bp
from api import redishelper
from api import constants
import datetime
from flask import request, render_template, redirect, url_for
import json
import logging

def link_details(id, describe = False):
    logging.info(f"id : {id}")
    err, link = redishelper.get_key(id)
    if err:
        return paragraph_tag(err)
    if link:
        link = json.loads(link)
        if describe:
            return link
        else:
            link = link.get(constants.URL_PARAMS_LINK)
            return redirect(f"{link}")
    return paragraph_tag("Empty")


def request_validator(req):
    try:
        if len(req.form) == 0:
            return paragraph_tag("Empty data sent")
        if req.form.get(constants.URL_PARAMS_LINK) is None:
            return paragraph_tag(f"{constants.URL_PARAMS_LINK} doesn't exist")
        if req.form.get(constants.URL_PARAMS_ALIAS) is None:
            return paragraph_tag(f"{constants.URL_PARAMS_ALIAS} doesn't exist")
        http_string = "http://"
        https_string = "https://"
        link = req.form.get(constants.URL_PARAMS_LINK)
        if len(link) < len(http_string) or \
                link[:len(http_string)] != http_string and \
                link[:len(https_string)] != https_string:
            return paragraph_tag("link must start with http or https")
    except Exception as e:
            logging.critical(f"Couldn't parse data due to {str(e)}")
            return paragraph_tag("Couldn't parse data")
    return None

def request_edit_validator(req):
    try:
        if len(req.form) == 0:
            return paragraph_tag("Empty data sent")
        if req.form.get(constants.URL_PARAMS_LINK) is None:
            return paragraph_tag(f"{constants.URL_PARAMS_LINK} doesn't exist")
        if req.form.get(constants.URL_PARAMS_EDIT_OLD_ALIAS) is None:
            return paragraph_tag(f"{constants.URL_PARAMS_EDIT_OLD_ALIAS} doesn't exist")
        if req.form.get(constants.URL_PARAMS_EDIT_NEW_ALIAS) is None:
            return paragraph_tag(f"{constants.URL_PARAMS_EDIT_NEW_ALIAS} doesn't exist")
        http_string = "http://"
        https_string = "https://"
        link = req.form.get(constants.URL_PARAMS_LINK)
        if len(link) < len(http_string) or \
                link[:len(http_string)] != http_string and \
                link[:len(https_string)] != https_string:
            return paragraph_tag("link must start with http or https")
    except Exception as e:
            logging.critical(f"Couldn't parse data due to {str(e)}")
            return paragraph_tag("Couldn't parse data")
    return None

def paragraph_tag(text):
    return text