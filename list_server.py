import argparse
import datetime
import json
import os
import re

from os import path

import bottle
from bottle import (
        abort,
        auth_basic,
        default_app,
        get,
        hook,
        post,
        redirect,
        request,
        response,
        route,
        run,
        static_file,
        template,
    )

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

config = None

def check_auth(username, password):
    return username == config['username'] and \
            password == config['password']


# list crud endpoints
@get('/')
def index():
    all_lists = get_all_list_names()

    return template("index.tpl", title="index", lists=sorted(all_lists))


@get('/l/<name:re:[a-z0-9-_]+>')
def list_view(name):
    validate_list(name)

    list_contents = get_list(name)

    return template("list.tpl", list_name=name, list_contents=list_contents)


@post('/l/<name:re:[a-z0-9-_]+>/update')
@auth_basic(check_auth)
def list_update(name):
    list_item_text = request.forms.get('list_item_text', None)

    if list_item_text is None:
        abort(400, "List item not specified")


    validate_list(name)

    new_item = {
        "text": list_item_text,
        "creation_date": datetime.datetime.now().isoformat(),
        "is_checked": False
    }

    list_contents = get_list(name)
    list_contents.append(new_item)

    update_list(name, list_contents)

    redirect("/l/" + name)


@get('/l/<name:re:[a-z0-9-_]+>/delete/<index:int>')
@auth_basic(check_auth)
def list_item_delete(name, index):
    validate_list(name)

    list_contents = get_list(name)
    del list_contents[index]

    update_list(name, list_contents)

    redirect("/l/" + name)


@get('/l/<name:re:[a-z0-9-_]+>/check/<index:int>')
@auth_basic(check_auth)
def list_item_check(name, index):
    validate_list(name)

    list_contents = get_list(name)

    list_contents[index]['is_checked'] = not list_contents[index]['is_checked']

    update_list(name, list_contents)

    response.status = 303
    response.set_header('Location', "/l/" + name)


@get('/l/<name:re:[a-z0-9-_]+>/clearchecked')
@auth_basic(check_auth)
def list_clear_checked(name):
    validate_list(name)

    new_list = [x for x in get_list(name) if not x['is_checked']]
    update_list(name, new_list)

    redirect("/l/" + name)


@post('/s/add')
@auth_basic(check_auth)
def list_add():
    name = request.forms.get('list_name', None).lower()

    if name is None:
        abort(400, "List name not specified")

    all_lists = get_all_list_names()
    if name in all_lists:
        abort(400, "List already exists")

    update_list(name, [])

    redirect("/l/" + name)


@post('/s/delete')
@auth_basic(check_auth)
def list_delete():
    name = request.forms.get('list_name', None).lower()
    if name is None:
        abort(400, "List name not specified")

    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(400, "List does not exists")

    delete_list(name)
    redirect("/")


# list file operations
def get_all_list_names():
    return [x.split(".")[0] for x in os.listdir(config['data_path'])]


def update_list(name, list_contents):
    with open(get_list_file_loc(name), "w") as f:
        json.dump(list_contents, f, indent=4, sort_keys=True)


def get_list(name):
    with open(get_list_file_loc(name), "r") as f:
        return json.load(f)


def delete_list(name):
    os.remove(get_list_file_loc(name))


def get_list_file_loc(name):
    filename = name + ".json"
    fileloc = path.join(config['data_path'], filename)

    return fileloc


def validate_list(name):
    if re.match(r"[a-z0-9-_]+", name) is None:
        abort(400, "Invalid list name")

    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(404, "List not found")


# misc
@route('/static/<path:path>')
def static(path):
    return static_file(path, root=get_script_rel_path("static"))

def get_script_rel_path(filepath):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return path.join(script_dir, filepath)


# remove ending slash from requests
@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

tpl_path = path.join(get_script_rel_path("templates"))
bottle.TEMPLATE_PATH.insert(0, tpl_path)
try:
    with open(get_script_rel_path("config.json")) as f:
        config = json.load(f)
except:
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='starts a lists server')
    parser.add_argument('--config', help='specifies the config file location (default: ./config.json)',
                            default="./config.json")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    run(host='0.0.0.0', port=config['port'])

app = default_app()
