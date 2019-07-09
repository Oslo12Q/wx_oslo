#!/usr/bin/python
#-*- coding: UTF-8 -*- 
#coding=utf-8

import hashlib
import json
import datetime
import urllib2
import urllib
import random
from xml.etree import ElementTree
from django.utils.encoding import smart_str
from django.http import HttpResponse
from . import utils
from wx_oslo.settings import AppID,AppSecret

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
    print MsgType
    if MsgType == 'text':
        Content = xml.find('Content').text
        print Content
        msg = '2'
    elif MsgType == 'event':
        msg = '欢迎关注Oslo测试号,目前还在建设中~~~~'
    else:
        msg = 'Oslo还在建设中~~~'
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

tok = fetchJsApiTicket()
print tok