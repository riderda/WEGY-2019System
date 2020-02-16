import urllib.parse
import http.cookiejar
import urllib.request
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def question(question):
    url = "http://150s.cn"

    resp = requests.get(url)
    cookies = resp.cookies
    p = ('; '.join(['='.join(item) for item in cookies.items()]))
    cj = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)
    url = "http://150s.cn/topic/getSubject"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
        'Cookie': p,
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    data = {
        'title': question,
    }
    request = urllib.request.Request(url=url,headers =headers)
    data = urllib.parse.urlencode(data).encode()
    response = opener.open(request, data)
    data = response.read().decode()
    print(data)
    return data

