from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

# DB 연결 코드
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root1234',
    db='mini',
    charset='utf8'
)

# JWT 토큰을 만들 때 필요한 비밀문자열
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'freeExhib'

# JWT 패키지를 사용합니다.
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 비밀번호를 암호화하여 DB에 저장
import hashlib

# HTML을 주는 부분
@app.route('/')
def home():
    # 쿠키에서 토큰 받아올 때
    tokenReceive = request.cookies.get('mytoken')

    return render_template('index.html', token=tokenReceive)



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


# 로그인, 회원가입을 위한 API

# [회원가입 API]
# uesrId, pwd를 받아서, DB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/users/register', methods=['POST'])
def apiRegister():
    idReceive = request.form['userId_give']
    pwReceive = request.form['userPw_give']
    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()

    with conn.cursor() as cursor:
        sql = "INSERT INTO users (userId,pwd) VALUES (%s,%s)"
        cursor.execute(sql, (idReceive, pwHash))
        conn.commit()
        return jsonify({'result': 'success'})

@app.route('/users/checkDup', methods=['POST'])
def checkDup():
    userReceive = request.form['userid_give']

    with conn.cursor() as cursor:
        sql = "SELECT * FROM users where userId = %s"
        cursor.execute(sql, (userReceive))
        user = cursor.fetchone()
        exists = bool(user)

    return jsonify({'result': 'success', 'exists': exists})

# [로그인 API]
# userId, pwd를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/users/login', methods=['POST'])
def apiLogin():
    idReceive = request.form['userId_give']
    pwReceive = request.form['userPw_give']
    pwHash = hashlib.sha256(pwReceive.encode('utf-8')).hexdigest()

    # userId, pwd를 DB에서 찾습니다.
    with conn.cursor() as cursor:
        sql = "SELECT * FROM users where userId = %s AND pwd = %s"
        cursor.execute(sql, (idReceive, pwHash))
        result = cursor.fetchone()

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'userId': idReceive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # # 토큰값을 users DB에 저장하여 줍니다.
        # with conn.cursor() as cursor:
        #     sql = "UPDATE users SET jwtToken=%s WHERE userId=%s"
        #     cursor.execute(sql, (token, idReceive))
        #     conn.commit()

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
