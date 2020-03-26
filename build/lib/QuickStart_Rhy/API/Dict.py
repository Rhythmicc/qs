import requests
import execjs
import re

JS_CODE = """function a(r, o) { for (var t = 0; t < o.length - 2; t += 3) { var a = o.charAt(t + 2); a = a >= "a" 
    ? a.charCodeAt(0) - 87 : Number(a), a = "+" === o.charAt(t + 1) ? r >>> a: r << a, r = "+" === o.charAt(t) ? r + 
    a & 4294967295 : r ^ a } return r } var C = null; var token = function(r, _gtk) { var o = r.length; o > 30 && (r 
    = "" + r.substr(0, 10) + r.substr(Math.floor(o / 2) - 5, 10) + r.substring(r.length, r.length - 10)); var t = 
    void 0, t = null !== C ? C: (C = _gtk || "") || ""; for (var e = t.split("."), h = Number(e[0]) || 0, i = Number(
    e[1]) || 0, d = [], f = 0, g = 0; g < r.length; g++) { var m = r.charCodeAt(g); 128 > m ? d[f++] = m: (2048 > m ? 
    d[f++] = m >> 6 | 192 : (55296 === (64512 & m) && g + 1 < r.length && 56320 === (64512 & r.charCodeAt(g + 1)) ? (
    m = 65536 + ((1023 & m) << 10) + (1023 & r.charCodeAt(++g)), d[f++] = m >> 18 | 240, d[f++] = m >> 12 & 63 | 128) 
    : d[f++] = m >> 12 | 224, d[f++] = m >> 6 & 63 | 128), d[f++] = 63 & m | 128) } for (var S = h, u = "+-a^+6", 
    l = "+-3^+b+-f", s = 0; s < d.length; s++) S += d[s], S = a(S, u); return S = a(S, l), S ^= i, 0 > S && (S = (
    2147483647 & S) + 2147483648), S %= 1e6, S.toString() + "." + (S ^ h) } """


class Dict:
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/71.0.3578.98 Safari/537.36 '
        }
        self.token = None
        self.gtk = None
        self.javascript = execjs.compile(JS_CODE)
        self.loadMainPage()
        self.loadMainPage()

    def loadMainPage(self):
        url = 'https://fanyi.baidu.com'
        try:
            r = self.sess.get(url, headers=self.headers)
            self.token = re.findall(r"token: '(.*?)',", r.text)[0]
            self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        except Exception as e:
            raise e

    def langdetect(self, query):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query': query}
        try:
            r = self.sess.post(url=url, data=data)
        except Exception as e:
            raise e

        json = r.json()
        if 'msg' in json and json['msg'] == 'success':
            return json['lan']
        return None

    def dictionary(self, query, dst='zh', src=None):
        url = 'https://fanyi.baidu.com/v2transapi'
        sign = self.javascript.call('token', query, self.gtk)
        if not src:
            src = self.langdetect(query)
        data = {
            'from': src,
            'to': dst,
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.token,
        }
        try:
            r = self.sess.post(url=url, data=data)
        except Exception as e:
            raise e
        if r.status_code == 200:
            json = r.json()
            if 'error' in json:
                raise Exception('baidu sdk error: {}'.format(json['error']))
            return json
        return None
