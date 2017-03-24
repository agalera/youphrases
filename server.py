from bottle import post, get, delete, request, HTTPError, run
from subprocess import call
import json
from moviepy.editor import AudioFileClip
import os


BASE = "/w"
DB_PATH = os.path.join(BASE, 'db.json')
if os.path.exists(DB_PATH):

    with open(DB_PATH) as data_file:
        db = json.load(data_file)
else:
    db = {}


@post('/')
def add():
    data = request.json

    for check in ['id', 'init', 'end', 'name']:
        if check not in data:
            return HTTPError(400)

    # if data['name'] in db:
    #     return HTTPError(302)

    _id = data['name']

    filename = "%s.mp3" % _id
    call(["youtube-dl", "-o",
          os.path.join(BASE, "tmp_" + filename),
          "-f", "bestaudio",
          "http://www.youtube.com/watch?v=%s" % data['id']])

    full_clip = AudioFileClip(os.path.join(BASE, "tmp_" + filename))
    subclip = full_clip.subclip(data['init'], data['end'])
    subclip.write_audiofile(os.path.join(BASE, filename))

    os.remove(os.path.join(BASE, "tmp_" + filename))

    db[_id] = {'yt_id': data['id'],
               'filename': os.path.join(BASE, filename)}

    save()
    if data.get('play'):
        play(_id)


@delete('/<id>')
def remove(id):
    if id in db:
        os.remove(db[id]['filename'])
        del db[id]
        save()


@get('/')
def all():
    return db


@get('/play/<id>')
def play(id):
    if id not in db:
        return HTTPError(404)

    print("play %s" % db[id])
    call(['play', db[id]['filename']])


def save():
    with open(DB_PATH, 'w') as outfile:
        json.dump(db, outfile)


run(host='0.0.0.0', port=9999)
