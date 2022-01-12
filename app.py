from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

import pymysql

app = Flask(__name__)

conn = pymysql.connect(host='localhost', user='root',
                       password='root1234', charset='utf8',
                       db='mini')

cursor = conn.cursor(pymysql.cursors.DictCursor);

# JWT 토큰을 만들 때 필요한 비밀문자열
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'freeExhib'

# JWT 패키지를 사용합니다.
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 비밀번호를 암호화하여 DB에 저장
import hashlib


@app.route('/detail/<id>')
def getDetail(id):
    getIdSql = "select exhibitionId from exhibitions where exhibitionId =%s"

    cursor.execute(getIdSql, id)

    getId = cursor.fetchone();
    print(getId)

    if not getId: return render_template("index.html")

    getExhibitionSql = "select * from exhibitions where exhibitionId = %s"

    cursor.execute(getExhibitionSql, id)

    exhibition = cursor.fetchone()
    print(exhibition)

    return render_template("detail.html", exhibition=exhibition)


@app.route('/reviews/<id>', methods=['GET'])
def getReviews(id):

    # 토큰의 만료기간이 다되면 만료 오류가 발생하였다
    # jwt access token 과 refresh token을 사용하거나
    # 유효성 검사를 만들어 토큰을 재발급하는 함수를 만들고 싶지만 시간이 부족하다


    getReviewSql = "select * from reviews where exhibitionId =%s"
    cursor.execute(getReviewSql, id)

    reviews = cursor.fetchall()
    print(reviews)
    # return jsonify({'allReviews': reviews, 'token': tokenReceive, 'userId': user})
    return jsonify({'allReviews': reviews})


# def validateToken():
#     tokenReceive = request.cookies.get('mytoken')
#     validate = jwt.decode(tokenReceive, SECRET_KEY, algorithms=['HS256'])
#     print(validate)


@app.route('/reviews', methods=['POST'])
def postReview():
    try:

        tokenReceive = request.cookies.get('mytoken')

        print(tokenReceive)

        payload = jwt.decode(tokenReceive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        with conn.cursor() as cursor:
            getUsrIdSql = "SELECT * FROM users where userId = %s"
            cursor.execute(getUsrIdSql, (payload['userId']))
            user = cursor.fetchone()
            print(user);

            userId = user[0]
            contentRecieve = request.form['content_give']
            exIdRecieve = request.form['exhibitionId_give']

            postSql = "insert into reviews ( userId,exhibitionId, content) values ( %s, %s, %s)"
            cursor.execute(postSql, (userId, exIdRecieve, contentRecieve))
            setSql = "SET @CNT = 0"
            cursor.execute(setSql)
            sortSql = "UPDATE reviews SET reviews.reviewId = @CNT:=@CNT+1;"
            cursor.execute(sortSql)

            conn.commit()
            return jsonify({'msg': '리뷰 작성'})
    except jwt.ExpiredSignatureError:
        return jsonify({'msg': '안돼'})
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 작성자가 들어왔을 때 지우는 API
# 토큰이 있을 때만 가능하게 해야함

@app.route('/reviews/<id>', methods=['DELETE'])
def deleteReview(id):
    id = request.form['id_give']
    sql = "delete from reviews where reviewId= %s"
    cursor.execute(sql, id)
    setSql = "SET @CNT = 0"
    cursor.execute(setSql)
    sortSql = "UPDATE reviews SET reviews.reviewId = @CNT:=@CNT+1;"
    cursor.execute(sortSql)
    conn.commit()
    return jsonify({'msg': '삭제 완료!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
