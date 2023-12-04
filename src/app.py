from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import sys
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv

import pymysql

config_map = {
    'user':'CMSC508_USER',
    'password':'CMSC508_PASSWORD',
    'host':'CMSC508_HOST',
    'database':'FLASK_DATABASE'
}

load_dotenv()
config = {}
for key in config_map.keys():
    config[key] = os.getenv(config_map[key])
flag = False
for param in config.keys():
    if config[param] is None:
        flag = True
        print(f"Missing {config_map[param]} in .env file")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://23FA_farzanrl:Shout4_farzanrl_GOME@cmsc508.com/23FA_groups_group32'
db = SQLAlchemy(app)

@app.route('/users', methods=['GET'])
def get_users():
    query = text("SELECT * FROM user;")
    result = db.session.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    user_list = [dict(zip(columns, row)) for row in rows]
    return jsonify(users=user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    query = text("SELECT * FROM user WHERE id = :user_id;")
    result = db.session.execute(query, {'user_id': user_id})
    row = result.first()
    if row:
        columns = result.keys()
        user_data = dict(zip(columns, row))
        return jsonify(user=user_data)
    else:
        return jsonify(message='User not found'), 404

@app.route('/artists', methods=['GET'])
def get_artists():
    query = text("SELECT * FROM artist;")
    result = db.session.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    artist_list = [dict(zip(columns, row)) for row in rows]
    return jsonify(artists=artist_list)

@app.route('/songs', methods=['GET'])
def get_songs():
    query = text("SELECT * FROM song;")
    result = db.session.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    song_list = [dict(zip(columns, row)) for row in rows]
    return jsonify(songs=song_list)

if __name__ == '__main__':
    app.run(debug=True)