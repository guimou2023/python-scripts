#!/usr/local/bin/env python
# -*- coding:utf-8 -*-
# __author__:"Howard"
import sys
from flask import Flask,request,Response
from utils.WXBizMsgCrypt import WXBizMsgCrypt
import json
import urllib
import urllib2
from werkzeug.contrib.cache import SimpleCache

# from wechatpy.enterprise import create_reply, parse_message
# from wechatpy.enterprise.crypto import WeChatCrypto

app = Flask(__name__)

# 假设企业在企业微信后台上设置的参数如下
sAgent_id = "1000002"
sCorpID = "ww532b5887083931ac"
sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
sSecret = "S0zjZTT7lnk48cC5y6PWVXpZJVKtGly2c1zJt5Fm1Rs"

wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
cache = SimpleCache()



def getToken():
    params_dic = {'corpid': sCorpID, 'corpsecret': sSecret}
    url_params = urllib.urlencode(params_dic)
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?" + url_params
    try:
            req_obj = urllib2.Request(url)
    except KeyError:
            raise KeyError
    result = urllib2.urlopen(req_obj)
    access_token_dic = json.load(result)
    return access_token_dic['access_token'],access_token_dic['expires_in']



@app.route('/auth', methods=['GET', 'POST'])
def auth():
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echo_str)
    if ret != 0:
        print "ERR: VerifyURL ret: " + str(ret)
        sys.exit(1)
    print sEchoStr
    return sEchoStr


@app.route('/send', methods=['GET', 'POST'])
def sendMessage():
    if request.method == 'POST':
        # 从缓存取token
        token = cache.get('token')
        if token is None:
            token,expires_in = getToken()
            cache.set('token', token, timeout=expires_in)

        tos = request.form.get('tos', '')
        message = request.form.get('content', '')
        data = json.dumps({
                'touser': tos,
                'msgtype': "text",
                'agentid': sAgent_id,
                'text':{
                    'content':message
                },
                'safe':"0"
        }, ensure_ascii=False)

        send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" %token
        print data,send_url
        req_obj = urllib2.Request(send_url, data)
        try:
            result = urllib2.urlopen(req_obj)
        except urllib2.HTTPError as e:
                if hasattr(e, 'reason'):
                    print 'reason', e.reason
                elif hasattr(e,'code'):
                    print 'code', e.code
        else:
            response_msg = json.load(result)
            result.close()
        return Response(json.dumps(response_msg), mimetype='application/json')

    elif request.method == 'GET':
        print request.args
        return "GET"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4567)

