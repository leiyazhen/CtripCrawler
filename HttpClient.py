import httplib2;
from urllib.parse import urlencode;

'''
http请求调用
'''
def httpCall(url, method, body, heads):
    try:
        h = httplib2.Http();
        (resp, content) = h.request(url, method, urlencode(body), heads);
        return (resp, content.decode('utf-8'));
    except Exception as e:
        print('http request error occours:' + repr(e));
        return None;
