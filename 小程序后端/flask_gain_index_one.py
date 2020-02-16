import re
import urllib.parse
import urllib.request
import http.cookiejar
import requests
import json
import pymysql.cursors
import threading
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def curriculum(opener,headers):
    c_data=''
    try:#课表爬虫
        get2_url = 'http://210.38.250.43/xsgrkbcx!getDataList.action'
        data = {
            'xnxqdm': "201902",
            'page': '1',
            'rows': '1000',
            'sort': 'kxh',
            'order': 'asc',
        }
        request = urllib.request.Request(url=get2_url,headers=headers)
        data = urllib.parse.urlencode(data).encode()
        response = opener.open(request,data)
        kb = response.read().decode()

        pattern = re.compile(r'"rows":\[{(.*?)}\]')
        curriculum_html = list(pattern.findall(kb))
        t = curriculum_html[0]
    except:
        c_data = '[]'
    else:
        if curriculum_html[0] == "":
            c_data = '[]'
        else:
            c_data = "[{" + curriculum_html[0] + "}]"

    return c_data

def achievement(opener,headers):
    a_data=''
    try:
        get_url = 'http://210.38.250.43/xskccjxx!getDataList.action'
        data={
            'xnxqdm':'',
            'page':	'1',
            'rows':	'100',
            'sort':	'xnxqdm,kcbh,ksxzdm',
            'order':	'asc',
        }
        request = urllib.request.Request(url=get_url,headers=headers)
        data = urllib.parse.urlencode(data).encode()
        response = opener.open(request,data)
        html_data = response.read().decode()
        pattern_html = re.compile(r'"xsxm":"(.*?)"')#正则
        pattern_time = re.compile(r'"xnxqmc":"(.*?)"')#
        a_time = list(pattern_time.findall(html_data))
        student_name = list(pattern_html.findall(html_data))#用户名字
        pattern_achievement = re.compile(r'"zcj":"(.*?)"')
        pattern_type = re.compile(r'"kcdlmc":"(.*?)"')
        pattern_state = re.compile(r'"ksxzmc":"(.*?)"')
        pattern_name = re.compile(r'"kcmc":"(.*?)"')
        pattern_point = re.compile(r'"cjjd":"(.*?)"')
        pattern_credit = re.compile(r'"xf":"(.*?)"')
        a_type = list(pattern_type.findall(html_data))
        a_state = list(pattern_state.findall(html_data))
        a_achievement = list(pattern_achievement.findall(html_data))
        a_name = list(pattern_name.findall(html_data))
        a_point = list(pattern_point.findall(html_data))
        a_credit = list(pattern_credit.findall(html_data))
        a_pd = a_name[0] #判断是否错误（关键）

    except:
        a_data = '[]'
    else:
        if (len(a_name) > 1):
            for n in range(len(a_name) - 1):
                a_data = '{' + '"a_name":"' + a_name[n] + '","a_point":"' + a_point[n] + '","a_time":"' + a_time[n] + '","a_achievement":"' + a_achievement[n] + '","a_type":"' + a_type[n] + '","a_state":"' + a_state[n] + '","a_credit":"' + a_credit[n] + '"},' + a_data
            a_data = '[' + a_data + '{' + '"a_name":"' + a_name[n + 1] + '","a_point":"' + a_point[n + 1] + '","a_time":"' + a_time[n + 1] + '","a_achievement":"' + a_achievement[n + 1] + '","a_type":"' + a_type[n + 1] + '","a_state":"' + a_state[n + 1] + '","a_credit":"' + a_credit[n + 1] + '"}' + ']'
        else:
            a_data = '[' + a_data + '{' + '"a_name":"' + a_name[0] + '","a_point":"' + a_point[0] + '","a_time":"' + a_time[0] + '","a_achievement":"' + a_achievement[0] + '","a_type":"' + a_type[0] + '","a_state":"' + a_state[0] + '","a_credit":"' + a_credit[0] + '"}' + ']'
    return a_data
def requset_quality(opener,headers):
    try:
        quality_data = ''
        get_url = 'http://210.38.250.43/xsktsbxx!getYxktDataList.action'
        data={
            'xnxqdm':'',
            'page': '1',
            'rows': '100',
            'sort': 'cjsj',
            'order':'desc',
        }
        request = urllib.request.Request(url=get_url,headers=headers)
        data = urllib.parse.urlencode(data).encode()
        response = opener.open(request,data)
        quality_data1 = response.read().decode()
        
        pattern = re.compile(r'{"i(.*?)}')
        quality_html = list(pattern.findall(quality_data1))
        for n in range(len(quality_html)-1):
            quality_data = '{"i' + quality_html[n] +'},' + quality_data
        quality_data = '['+ quality_data + '{"i' + quality_html[n+1] +'}]'
    except:
        return '[]'
    else:
        return quality_data
        

#开始请求
def requst_gain_index_one(code):
    try:

        appid="wxd1eacf33b4ed0195"
        secret="d23f76338f86a9818593c8e14872cb8a"
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
            "password":"1122qq33",
            "database":"userdata",
            "charset":"utf8"
        }
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql = "select * from userlogin where openid = '"+ openid + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            username = row[1]
            password = row[2]
        db.commit()  
        cursor.close()
        db.close()
        try:
            db = pymysql.connect(**config)
            cursor = db.cursor()
            sql = "select * from curriculum where id = '"+ username + "'"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                addcurriculum = row[1]
                decurriculum = row[2]
            db.commit()  
            cursor.close()
            db.close()
        except:
            addcurriculum = '[]'
            decurriculum = '[]'
        else:
            decurriculum = decurriculum
            addcurriculum = addcurriculum
        #保存cookies
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
        data = {
            'account': username,
            'pwd': pwd,
            'verifycode': '',
        }
        request = urllib.request.Request(url=url,headers=headers)
        data = urllib.parse.urlencode(data).encode()
        response = opener.open(request,data)
        html_login = response.read().decode()
        pattern = re.compile(r'"msg":"(.*?)"')
        html_login_if = str(pattern.findall(html_login))
        if(html_login_if==("['/login!welcome.action']")): #判断登陆
            request_data = '1'

            a = MyThread(achievement, (opener,headers,), achievement.__name__)

            c = MyThread(curriculum, (opener,headers,), curriculum.__name__)
            a.setDaemon(True)
            a.start()
            c.setDaemon(True)
            c.start()    
            a_data = a.get_result()


            c_data = c.get_result()
            t = MyThread(requset_quality, (opener,headers,), requset_quality.__name__)
            t.setDaemon(True)
            t.start()
            t_data = t.get_result()

        else:
            request_data = '"login":1,'
        if(request_data == '1'):

            gain_json = '{' +'"xuehao":"'+username+'",'+ '"login":1,' + '"achievement":' + a_data + ',"curriculum":' + c_data + ',"quality":' + t_data + ',"addcurriculum":'+ addcurriculum +',"decurriculum":'+ decurriculum + '}'

        else:
            gain_json = '{"login":0}'
        temp = json.loads(gain_json)
        gain_json = json.dumps(temp)
    except:
        gain_json = '{"login":0}'
        return gain_json
    else:
        return gain_json
    

