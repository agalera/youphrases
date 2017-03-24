from bottle import post, request, HTTPError, run
import uuid
from subprocess import call
import json
from moviepy.editor import AudioFileClip
import os


db = {}

@post('/add')
def add():
    data = request.json
    if ('id', 'init', 'end', 'name') not in data:
        return HTTPError(400)

    _id = uuid.uuid4()
    filename = "/w/%s.mp3" % _id
    call(["youtube-dl", "-o",
              "tmp_%s" % filename,
              "-f", "bestaudio",
              "http://www.youtube.com/watch?v=%s" % data['id']])

    clip = AudioFileClip("tmp_%s" % filename).sub_clip(data['init'], data['end'])
    clip.write_audiofile(filename)
    
    os.remove("tmp_%s" % filename)

    db[_id] = {'name': data['name'],
               'filename': filename}

    with open('db.json', 'w') as outfile:
        json.dump(db, outfile)

@get('/')
def all():
    return db

@get('/play/<id>')
def play(id):
    if id not in db:
        return HTTPError(404)

    print("play %s" % db[id])
    call(['play', db[id][filename]])

run(host='0.0.0.0', port=9999)
