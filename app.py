from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

# DB 연결 코드
import pymysql


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='mini',
    charset='utf8'
)


@app.route('/')
def home():

    return render_template('index.html')


##마이페이지 자신이 쓴 리뷰 보여주기
##자신이 찜 한 장소 보여주기
@app.route('/mypage')
def mypage():
    ## 인코딩 된 값을 디코딩 시켜줄 코드가 필요



    ##likes
    ##likes 테이블과 전시 테이블 right join
    ##userId와 페이로드에 id값이 같은 값들 전부 가져오기
    curs = conn.cursor()
    sql = "SELECT initDate, endDate, title, imgUrl " \
          "FROM mini.wishlist RIGHT JOIN mini.exhibition " \
          "on wishlist.exhibitionId2 = exhibition.exhibitionId " \
          "where userId2 = 'test'"


    ##review
    ##review 테이블과 전시 테이블 right join
    ##userId와 페이로드에 id값이 같은 값들 전부 가져오기
    sql2 = "SELECT content, imgUrl, title " \
           "FROM mini.review RIGHT JOIN mini.exhibition " \
           "on review.exhibitionId2 = exhibition.exhibitionId " \
           "where userId2 = 'test'" ##payload('[userId]')

    curs.execute(sql)
    likes = curs.fetchall()

    curs.execute(sql2)
    reviews = curs.fetchall()

    return render_template('mypage.html', likes = likes, reviews = reviews)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


conn.close()