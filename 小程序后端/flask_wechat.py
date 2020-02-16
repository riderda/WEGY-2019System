from flask import Flask, render_template, Response, request, send_file
import time
import flask_gain_index_one
import flask_login_index
import flask_addcurriculum
import flask_decurriculum
import flask_calendar
import flask_quit
import flask_question
import flask_message
import os

from flask_cors import *

# flask request连接
app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')  # 公告加载
def main():
    return '1'


@app.route('/question', methods=['POST'])  # 答案加载
def question():
    question = request.form.get('question')
    data = flask_question.question(question)
    return data


@app.route('/message')  # 公告加载
def message():
    message = flask_message.message()
    return message


@app.route('/quit', methods=['POST'])  # 退出
def quit():
    code = request.form.get('code')  # openid
    data = flask_quit.quit_one(code)
    return data


@app.route('/calendarpicture')  # 校历图片加载
def calendarpicture():
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file')
    img_stream = 'xl.png'
    file = os.path.join(filepath, img_stream)
    return send_file(file)


@app.route('/head/<file_key>')  # 头像图片加载
def head(file_key):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file')
    img_stream = file_key + '.png'
    file = os.path.join(filepath, img_stream)
    return send_file(file)


@app.route('/calendar')  # 校历加载1
def calendar():
    data = flask_calendar.calendar_one()
    return data


@app.route('/addcurriculum', methods=['POST'])  # 课表增加内容
def addcurriculum():
    code = request.form.get('code')  # openid
    curriculum = request.form.get('addcurriculum')
    data = flask_addcurriculum.addcurriculum_one(code, curriculum)
    return data


@app.route('/decurriculum', methods=['POST'])  # 学校课表删除内容
def decurriculum():
    code = request.form.get('code')  # openid
    curriculum = request.form.get('addcurriculum')
    data = flask_decurriculum.decurriculum_one(code, curriculum)
    return data


# 获取（成绩、课表、素拓）请求
@app.route('/gain_index_one', methods=['POST'])
def gain_index_one():
    code = request.form.get('code')  # openid
    data = flask_gain_index_one.requst_gain_index_one(code)
    return data


# 登陆判断
@app.route('/login_index', methods=['POST'])
def login_index():
    username = request.form.get('username')
    password = request.form.get('password')
    code = request.form.get('code')
    login_data = flask_login_index.login_index(username, password, code)
    return login_data



if __name__ == "__main__":
    app.run(threaded=True, port=5000, host='0.0.0.0', ssl_context=('wegy.crt', 'wegy.key'))

