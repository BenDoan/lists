import json
import os

from os import path

from bottle import route, run, template, request, abort

DATA_DIR = "data"

@route('/')
def index():
    all_lists = get_all_list_names()
    return template("templates/index.tpl", title="index", lists=all_lists)

@route('/l/<name:re:[a-z0-9-_]+>')
def list(name=None):
    if name is None:
        abort(400, "Missing list name")

    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(404, "List not found")

    list_contents = get_list(name)
    return template("templates/list.tpl", list_name=name, list_contents=list_contents)

def get_all_list_names():
    return [x.split(".")[0] for x in os.listdir(DATA_DIR)]

def update_list(name, list_contents):
    with open(get_fileloc(name), "w") as f:
        json.dump(list_contents)

def get_list(name):
    with open(get_fileloc(name), "r") as f:
        return json.load(f)

def get_fileloc(list_name):
    filename = list_name + ".json"
    fileloc = path.join(DATA_DIR, filename)

    return fileloc

if __name__ == '__main__':
    run(host='localhost', port=8080)
