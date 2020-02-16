import re
import urllib.parse
import urllib.request
import http.cookiejar
import requests
import json
import pymysql.cursors
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def login_index(username,password,code):
    #保存cookies
    pattern = re.compile(r'\d+')
    username = pattern.findall(username)[0]
    cj = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)
    url = "http://210.38.250.43/login!doLogin.action"
    resp = requests.get(url)
    cookies = resp.cookies
    p=('; '.join(['='.join(item) for item in cookies.items()]))
    #建立头文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        'Cookie': p,
    }
    #建立数值文件
    import pjtt
    pwd = pjtt.pj(password)
    data={
        'account':username,
        'pwd':pwd,
        'verifycode':'',
    }
    request = urllib.request.Request(url=url,headers=headers)
    data = urllib.parse.urlencode(data).encode()
    response = opener.open(request,data)
    html_login = response.read().decode()
    pattern = re.compile(r'"msg":"(.*?)"')
    html_login_if = str(pattern.findall(html_login))
    print(html_login_if)
    if(html_login_if==("['/login!welcome.action']")): #判断登陆
        appid="wxd1eacf33b4ed0195"
        secret=""
        request_data = '1'
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
        response = urllib.request.urlopen(url=url)
        openid = response.read().decode()
        pattern_openid = re.compile(r'"openid":"(.*?)"')
        openid = list(pattern_openid.findall(openid))
        openid = openid[0]
        config={
            "host":"127.0.0.1",
            "user":"root",
            "password":"",
            "database":"userdata",
            "charset":"utf8"
        }
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql = "REPLACE INTO userlogin(openid,username,password) VALUES(%s,%s,%s)"
        cursor.execute(sql,(openid,username,password))
        db.commit()
        cursor.close()
        db.close()
        try:
            db = pymysql.connect(**config)
            cursor = db.cursor()
            sql = "INSERT INTO curriculum(id) VALUES(%s)"
            cursor.execute(sql,(username))
            db.commit()
            cursor.close()
            db.close()
        except:
            None
        else:
            None
        gain_json = '{"login":1}'
    else:
        gain_json = '{"login":0}'
        temp = json.loads(gain_json)
        gain_json = json.dumps(temp)
    return gain_json



