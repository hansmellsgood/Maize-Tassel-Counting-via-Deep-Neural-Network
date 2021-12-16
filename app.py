import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return

if __name__ == '__main__':
    app.run(debug=True)

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def visit():
    if request.method == 'GET':

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM visits")

        res = cur.fetchall()

        return jsonify(res)

    if request.method == 'POST':
        name = request.json['visitor_name']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO visits (visitor_name) VALUES(%s)", [name])

        mysql.connection.commit()

        cur.close()
        return