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

    getIdSql = "select ex_id from exhibitions where ex_id =%s"

    cursor.execute(getIdSql, id)

    getId = cursor.fetchone();
    print(getId)


    # if not getId: return render_template("main.html")

    getExhibitionSql = "select * from exhibitions where ex_id = %s"

    cursor.execute(getExhibitionSql, id)

    exhibition = cursor.fetchone()
    print(exhibition)

    getReviewSql = "select * from reviews where review_id =%s"
    cursor.execute(getReviewSql, id)

    reviews = cursor.fetchall()
    print(reviews)

    return render_template("detail.html", exhibition=exhibition, reviews=reviews)

# 작성자가 들어왔을 때 지우는 API
# 토큰이 있을 때만 가능하게 해야함
@app.route('/reviews/<id>', methods=['DELETE'])
def deleteReview(id):
    id = request.form['id_give']
    sql = "delete from reviews where id= %s"
    cursor.execute(sql, id)
    cursor.fetchone()
    conn.commit()
    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)