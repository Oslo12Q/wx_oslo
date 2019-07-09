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
        dic = {u'平顶山',u'朝阳',u'海淀'}
        if Content in dic:
            ts = create_tag(Content)
            msg = '2'
        else:
            msg = 'Oslo还在建设中~~~'
    elif MsgType == 'event':
        msg = '欢迎关注Oslo测试号,目前还在建设中~~~~'
    else:
        msg = 'Oslo还在建设中~~~'
    return sendTxtMsg(FromUserName,ToUserName,msg)

## 转化格式
def sendTxtMsg(FromUserName,ToUserName,Content):
    reply_xml = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),Content)
    
    return HttpResponse(reply_xml)

##获取access_token
def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    AppID, AppSecret)
    result = urllib2.urlopen(url).read()
    access_token = json.loads(result).get('access_token')
    return access_token

## 获取所有标签
def get_tags(request):
    tag_name = u'广东'
    access_token = get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token='+access_token
    result = urllib2.urlopen(url).read()
    jso = json.loads(result).get('tags')
    for i in jso:
        if tag_name in i.get('name'):
            print '我以存在'
        else:
            print '我不在'
            tg = create_tag(tag_name)
    return HttpResponse("Hello World")


# 创建标签
def create_tag(tags):
    access_token = get_token()
    print access_token
    url = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token='+access_token
    req = urllib2.Request(url)
    data = {
        "tag":{
                "name":tags
        }
    }
    print data
    req.add_header('Content-Type', 'application/json')
    req.add_header('encoding', 'utf-8')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    print result
    return result




