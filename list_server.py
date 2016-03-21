import json
import os

from os import path

from bottle import (
        route,
        run,
        template,
        request,
        abort,
        get,
        post,
        redirect
    )

DATA_DIR = "data"


@get('/')
def index():
    all_lists = get_all_list_names()
    return template("templates/index.tpl", title="index", lists=all_lists)


@get('/l/<name:re:[a-z0-9-_]+>')
def list_view(name):
    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(404, "List not found")

    list_contents = get_list(name)
    return template("templates/list.tpl", list_name=name, list_contents=list_contents)


@post('/l/<name:re:[a-z0-9-_]+>/update')
def list_update(name):
    list_item = request.forms.get('list_item', None)

    if list_item is None:
        abort(400, "List item not specified")


    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(404, "List not found")

    list_contents = get_list(name)
    list_contents.append(list_item)

    update_list(name, list_contents)

    redirect("/l/" + name)


@get('/l/<name:re:[a-z0-9-_]+>/delete/<index:int>')
def list_delete(name, index):
    all_lists = get_all_list_names()
    if name not in all_lists:
        abort(404, "List not found")

    list_contents = get_list(name)
    del list_contents[index]

    update_list(name, list_contents)

    redirect("/l/" + name)


@post('/s/add')
def list_add():
    name = request.forms.get('list_name', None)

    if name is None:
        abort(400, "List name not specified")

    all_lists = get_all_list_names()
    if name in all_lists:
        abort(400, "List already exists")

    update_list(name, [])

    redirect("/l/" + name)


def get_all_list_names():
    return [x.split(".")[0] for x in os.listdir(DATA_DIR)]


def update_list(name, list_contents):
    with open(get_fileloc(name), "w") as f:
        json.dump(list_contents, f)


def get_list(name):
    with open(get_fileloc(name), "r") as f:
        return json.load(f)


def delete_list(name):
    os.remove(get_fileloc(name))


def get_fileloc(name):
    filename = name + ".json"
    fileloc = path.join(DATA_DIR, filename)

    return fileloc


if __name__ == '__main__':
    run(host='localhost', port=8080)