import re
import urllib.parse
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import pymysql.cursors


def addcurriculum_one(code, data):
    try:
        appid = "wxd1eacf33b4ed0195"
        secret = ""
        request_data = '1'
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
        response = urllib.request.urlopen(url=url)
        openid = response.read().decode()
        pattern_openid = re.compile(r'"openid":"(.*?)"')
        openid = list(pattern_openid.findall(openid))
        openid = openid[0]
        config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "userdata",
            "charset": "utf8"
        }
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql = "select * from userlogin where openid = '" + openid + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            username = row[1]
        db.commit()
        cursor.close()
        db.close()
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql = "UPDATE curriculum SET addcurriculum='" + data + "' where id ='" + username + "'"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    except:
        json = '{"decide":0}'
        return json
    else:
        json = '{"decide":1}'
        return json
