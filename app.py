from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import pymysql

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='root',
                       password='root1234', charset='utf8',
                       db='mini')

cursor = conn.cursor(pymysql.cursors.DictCursor);


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)