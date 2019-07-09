#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8

import hashlib
import json
from xml.etree import ElementTree
from django.utils.encoding import smart_str
from django.http import HttpResponse
import datetime
import urllib2
import urllib
import random
from . import utils
from django.shortcuts import render

TOKEN = 'weixin'

def weixin(request):
    print request.method
    if request.method == 'GET':
        return checkSignature(request)
    if request.method == 'POST':
        return parseTxtMsg(request)


def checkSignature(request):
    
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        return HttpResponse("Hello World")

def parseTxtMsg(request):

    xmlstr = smart_str(request.body)
    xml =ElementTree.fromstring(xmlstr)
    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime =xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text

    if MsgType == 'text':
	Content = xml.find('Content').text
	print 	Content
 	if Content == '1':
            number_of_records = KeyHua.objects.count()
            random_index = int(random.random()*number_of_records)+1
            random_paint = KeyHua.objects.filter(id = random_index)
            for i in random_paint:
                keys = i.key
       	    msg = keys
        elif Content == '2':
            msg = datetime.datetime.now()
        elif Content == '查看违章':
            msg = '点击<a href="http://oslo.obstinate.cn/dev/index/">违章查询</a>'
        else:
            msg = '欢迎关注刘志强的个人微信公众号！\n本公众号正在建设中。\n输入1听笑话。\n输入2查看当前时间,任意输入将重新收到本消息。\n功能如下：\n1.<a href="http://oslo.obstinate.cn/dev/index/">查询医院疾病等信息</a>。\n2.<a href="http://m.weizhang8.cn">违章查询</a>。\n3.<a href="http://oslo.obstinate.cn/oslo/">ocr识别正在研发中</a>'

    elif MsgType == 'image':
	    msg = '您发的图片我们已经收到。'
    elif MsgType == 'voice':
	    msg = '感谢您的留言，我们会尽快处理。'
    elif MsgType == 'video':
	    msg = '感谢您的留言，我们会尽快处理。'
    elif MsgType == 'shortvideo':
	    msg = '感谢您的留言，我们会尽快处理。'
    elif MsgType == 'location':
	    msg = '您当前尚未绑定设备哦，如需绑定，点击<a href="http://dev.yijiayinong.com/ceshi/">扫一扫</a>，对准设备上的二维码即可！'
    elif MsgType == 'link':
	    msg = '感谢您的留言，我们会尽快处理。'
    
    elif MsgType == 'event':
	    msgContent = xml.find('Event').text
	    if msgContent == 'subscribe':
	        msg = '欢迎关注刘志强的个人微信公众号！\n本公众号正在建设中。\n输入1听笑话。\n输入2查看当前时间,任意输入将重新收到本消息。\n功能如下：\n1.<a href="http://oslo.obstinate.cn/dev/index/">查询医院疾病等信息</a>。\n2.<a href="http://m.weizhang8.cn">违章查询</a>。\n3.<a href="http://oslo.obstinate.cn/oslo/">ocr识别正在研发中</a>'

	    if msgContent == 'unsubscribe':
	        msg = ''
	    
    return sendTxtMsg(FromUserName,ToUserName,msg)


def sendTxtMsg(FromUserName,ToUserName,Content):
    reply_xml = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),Content)
    
    return HttpResponse(reply_xml)


def getResponseImageTextXml(FromUserName, ToUserName,title,description,picurl,url):  
    
    reply_xml = """<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[news]]></MsgType>
	<ArticleCount>1</ArticleCount>
	<Articles>
	<item>
	    <Title><![CDATA[%s]]></Title>
	    <Description><![CDATA[%s]]></Description>
	    <PicUrl><![CDATA[%s]]></PicUrl>
	    <Url><![CDATA[%s]]></Url>
	</item>
	</Articles>
	</xml>"""%(FromUserName,ToUserName,datetime.datetime.now(),title,description,picurl,url)
    return HttpResponse(reply_xml)


AppID = 'wxeef13872d0ba56f6'

AppSecret = '0573d4b276a55257f8ac6e6a69df1385'


##获取access_token
def get_token():

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    AppID, AppSecret)
    result = urllib2.urlopen(url).read()
    access_token = json.loads(result).get('access_token')
    print access_token
    return access_token

def fetchJsApiTicket():
	access_token = get_token()
	if access_token is None:
		return None
	url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token='+access_token
	result1 = urllib2.urlopen(url).read()
        ticket = json.loads(result1).get('ticket')
	return ticket

def createWXConfig(jsApiList):
	nonceStr = utils.nonceStr()
	jsapi_ticket = fetchJsApiTicket()
	timestamp = str(utils.now())
	url = config.url
	d = {
		'noncestr': nonceStr,
		'jsapi_ticket': jsapi_ticket,
		'timestamp': timestamp,
		'url': url
	}
	signature = utils.generateSHA1Sign(d)
	dd = {
		'debug': False,
		'appId': AppID,
		'timestamp': timestamp,
		'nonceStr': nonceStr,
		'signature': signature,
		'jsApiList': jsApiList
	}
	return dd

def weixinJsapi(request):

    jsApiList = request.GET.get('jsApiList', None)
    data = createWXConfig(jsApiList)
    return Response(data)
    
    

def create1WXConfig(jsApiList):
        nonceStr = utils.nonceStr()
        jsapi_ticket = fetchJsApiTicket()
        timestamp = str(utils.now())
        url = config.url1
        d = {
                'noncestr': nonceStr,
                'jsapi_ticket': jsapi_ticket,
                'timestamp': timestamp,
                'url': url
        }
        signature = utils.generateSHA1Sign(d)
        dd = {
                'debug': False,
                'appId': AppID,
                'timestamp': timestamp,
                'nonceStr': nonceStr,
                'signature': signature,
                'jsApiList': jsApiList
        }
        return dd

def weixin1Jsapi(request):

    jsApiList = request.GET.get('jsApiList', None)
    data = create1WXConfig(jsApiList)
    return Response(data)


##创建自定义菜单	
def createMenu(request):
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % get_token()
    print url
    data = {
        "button": [
            {
                "type": "view",
                "name": "查询",
                "url": "http://oslo.obstinate.cn/dev/index/"
            },
            {
                "type": "view",
                "name": "history",
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzAwMzk1OTQzMg==&scene=124#wechat_redirect"
            }
        ]
    }

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    return HttpResponse(result)



