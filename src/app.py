from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
import os
import sys
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv
from IPython.display import display, Markdown
import pymysql
from datetime import time
import json
# note to self: add ?token=285247389 for user authentication

# to run this file, must go to myEnv->Scripts at type "activate" in the command line
# then go to src and run "python app.py"
# for dates, use DATE_FORMAT(attributeName, '%M %D, %Y') AS attributeName
# for times, use TIME_FORMAT(attributeName, '%H:%i') AS attributeName

# the following code is from the hw9.qmd file

# configuring .env
# make sure to add FLASK_DATABASE to your .env file
config_map = {
    'user':'CMSC508_USER',
    'password':'CMSC508_PASSWORD',
    'host':'CMSC508_HOST',
    'database':'FLASK_DATABASE'
}
# load and store credentials
load_dotenv()
config = {}
for key in config_map.keys():
    config[key] = os.getenv(config_map[key])
flag = False
for param in config.keys():
    if config[param] is None:
        flag = True
        print(f"Missing {config_map[param]} in .env file")

# build a sqlalchemy engine string
engine_uri = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

# connecting to the database
try:
    conn = create_engine(engine_uri)
except ArgumentError as e:
    print(f"create_engine: Argument Error: {e}")
    #sys.exit(1)
except NoSuchModuleError as e:
    print(f"create_engine: No Such Module Error: {e}")
    #sys.exit(1)
except Exception as e:
    print(f"create_engine: An error occurred: {e}")
    #sys.exit(1)

# helper routines
def my_sql_statement( statement ):
    """ used with DDL, when the statement doesn't return any results. """
    try:
        with conn.begin() as x:
            x.execute(text(statement))
            x.commit()
        result = ""
    except Exception as e:
        result = f"Error: {str(e)}"
    return result


def testExecution(executionResult):
    rows = executionResult.fetchall()
    print("rows: ", rows)
    print()
    if rows:
        columns = executionResult.keys()
        print("columns: ", columns)
        return [dict(zip(columns, row)) for row in rows]
    else:
        return 0
    
def serialize_time(obj):
    print("hi ",obj)
    if isinstance(obj, time):
        return obj.strftime("%H:%M:%S")
    print("hi ",obj)
    raise TypeError("Type not serializable")

def iterateTest(list):
    for i in list:
        for j in i:
            print(j)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
db = SQLAlchemy(app)

# API Methods:

# User methods:

@app.route('/users', methods=['GET'])
def get_users():
    query = text("SELECT * FROM user;")
    user_list = testExecution(db.session.execute(query))
    iterateTest(user_list)
    if(user_list):
        return jsonify(users=user_list)
    return jsonify(message='No users have been added.'), 404

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    query = text("SELECT * FROM user WHERE id = :user_id;")
    user_list = testExecution(db.session.execute(query, {'user_id': user_id}))
    if(user_list):
        return jsonify(user=user_list)
    return jsonify(message='User not found.'), 404

# Artist methods:

@app.route('/artists', methods=['GET'])
def get_artists():
    query = text("SELECT * FROM artist;")
    artist_list = testExecution(db.session.execute(query))
    print(artist_list)
    if(artist_list):
        return jsonify(artists=artist_list)
    return jsonify(message='No artists have been added.'), 404

# Song methods:
# Select songs with filters (artist id, artist name, album id, album name, song name, key, tempo)
    # Key required, any key
# Add songs (required info + optional info)
    # Artist key required, can only add their own songs
# Remove songs
    # ^Same requirement
# Update songs (1 attribute at a time)
    # ^Same requirement

@app.route('/songs', methods=['GET'])
def get_songs():
    name_regex = request.args.get('name')
    tempo_regex = request.args.get('tempo')
    key_regex = request.args.get('key')
    plays_regex = request.args.get('plays')
    duration_regex = request.args.get('duration')
    artist_regex = request.args.get('artist')
    artist_id_regex = request.args.get('artist_id')
    album_regex = request.args.get('album')
    album_id_regex = request.args.get('album_id')
    query = text("SELECT song.ID, song.name, tempo, song_key, plays, TIME_FORMAT(song.duration, '%H:%i') AS duration, song.artist_ID, artist.name AS artist_name, album_ID, album.name AS album_name FROM song JOIN artist ON song.artist_ID = artist.ID JOIN album ON song.album_ID = album.ID WHERE"
                 "(song.name REGEXP :name_regex OR :name_regex IS NULL) AND"
                 "(song.tempo REGEXP :tempo_regex OR :tempo_regex IS NULL) AND"
                 "(song.song_key REGEXP :key_regex OR :key_regex IS NULL) AND"
                 "(song.plays REGEXP :plays_regex OR :plays_regex IS NULL) AND"
                 "(song.duration REGEXP :duration_regex OR :duration_regex IS NULL) AND"
                 "(artist.name REGEXP :artist_regex OR :artist_regex IS NULL) AND"
                 "(artist.ID REGEXP :artist_id_regex OR :artist_id_regex IS NULL) AND"
                 "(album.name REGEXP :album_regex OR :album_regex IS NULL) AND"
                 "(album.ID REGEXP :album_id_regex OR :album_id_regex IS NULL);")
    result = db.session.execute(query, {'name_regex': name_regex,'tempo_regex': tempo_regex,'key_regex': key_regex,'plays_regex': plays_regex,'duration_regex': duration_regex,'artist_regex': artist_regex,'artist_id_regex': artist_id_regex, 'album_regex': album_regex,'album_id_regex': album_id_regex})
    songs_list = [{'Song ID': song.ID, 'Name': song.name, 'Artist ID': song.album_ID, 'Artist': song.artist_name, 'Album ID': song.album_ID, 'Album': song.album_name, 'Duration': song.duration, 'Plays': song.plays, 'Tempo': song.tempo, 'Key': song.song_key} for song in result]
    if(songs_list):
        return jsonify(songs_list)
    return jsonify(message='No songs fulfill this criteria.'), 404


    
    """artist_name = request.args.get('artist')
    if artist_name:
        query = text("SELECT song.ID, song.name, tempo, song_key, plays, TIME_FORMAT(duration, '%H:%i') AS duration, artist_ID, artist.name, album_ID FROM song JOIN artist ON song.artist_ID = artist.ID WHERE artist.name = :artist_name;")
        song_list = testExecution(db.session.execute(query, {'artist_name': artist_name}))
        if(song_list):
            return jsonify(songs=song_list)
        return jsonify(message=':artist_name has no songs.'), 404
    query = text("SELECT ID, name, tempo, song_key, plays, TIME_FORMAT(duration, '%H:%i') AS duration, artist_ID, album_ID FROM song WHERE id <= 20;")
    song_list = testExecution(db.session.execute(query))
    if(song_list):
        return jsonify(songs=song_list)
    return jsonify(message='No songs have been added.'), 404"""

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song_by_id(song_id):
    query = text("SELECT ID, name, tempo, song_key, plays, TIME_FORMAT(duration, '%H:%i') AS duration, artist_ID, album_ID FROM song WHERE id = :song_id;")
    song_list = testExecution(db.session.execute(query, {'song_id': song_id}))
    if(song_list):
        return jsonify(songs=song_list)
    return jsonify(message='Song not found.'), 404

@app.route('/songs/?artist=<string:artist_name>', methods=['GET'])
def get_song_by_artist(artist_name):
    query = text("SELECT ID, name, tempo, song_key, plays, TIME_FORMAT(duration, '%H:%i') AS duration, artist_ID, album_ID FROM song JOIN (SELECT ID, name FROM artist) ON song.artistID = artist.ID WHERE artist.name = :artist_name;")
    song_list = testExecution(db.session.execute(query, {'artist_name': artist_name}))
    if(song_list):
        return jsonify(songs=song_list)
    return jsonify(message=':artist_name has no songs.'), 404

# Album methods:

@app.route('/albums', methods=['GET'])
def get_albums():
    query = text("SELECT ID, name, record_label, genre, DATE_FORMAT(release_date, '%M %D, %Y') AS release_date, classification, TIME_FORMAT(duration, '%H:%i') AS duration, artist_ID FROM album;")
    album_list = testExecution(db.session.execute(query))
    if(album_list):
        return jsonify(albums=album_list)
    return jsonify(message='No albums have been added.'), 404

# Playlist methods:

@app.route('/playlists', methods=['GET'])
def get_playlists():
    query = text("SELECT ID, name, description, TIME_FORMAT(duration, '%H:%i') AS duration, user_ID FROM playlist;")
    playlist_list = testExecution(db.session.execute(query))
    if(playlist_list):
        return jsonify(playlists=playlist_list)
    return jsonify(message='No playlists have been added.'), 404

if __name__ == '__main__':
    app.run(debug=True)