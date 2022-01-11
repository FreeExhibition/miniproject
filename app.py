from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import pymysql

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='root',
                       password='root1234', charset='utf8',
                       db='mini')

cursor = conn.cursor(pymysql.cursors.DictCursor);


@app.route('/detail/<id>')
def getDetail(id):
    getExhibitionSql = "select * from exhibitions where ex_id = %s"

    cursor.execute(getExhibitionSql, id)

    exhibition = cursor.fetchone()
    print(exhibition)

    getReviewSql = "select * from reviews where review_id =%s"
    cursor.execute(getReviewSql, id)

    reviews = cursor.fetchall()
    print(reviews)

    return render_template("detail.html", exhibition=exhibition, reviews=reviews)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
