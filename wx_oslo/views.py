#!/usr/bin/python
#-*- coding: UTF-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import hashlib
import json
import datetime
import urllib2
import urllib
import random
from xml.etree import ElementTree
from django.utils.encoding import smart_str
from django.http import HttpResponse
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
    openid = request.GET.get('openid') # 获取 openid

    if MsgType == 'text':
        Content = xml.find('Content').text
        dic = {u'平顶山',u'朝阳',u'海淀'}
        if Content in dic:
            ts = get_tags(Content)
            if ts is None:
                t_id = create_tag(Content)
                er = mob_create_tag(openid,t_id)
            else:
                er = mob_create_tag(openid,ts)
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


## 查询此标签是否存在
# 参数 tag_name 
# return / tag_id
def get_tags(tag_name):
    access_token = get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token='+access_token
    result = urllib2.urlopen(url).read()
    jso = json.loads(result).get('tags')
    for i in jso:
        if tag_name in i.get('name'):
            tag_id = i.get('id')
            return tag_id 
    return None
        
# 创建标签
# 参数 tag_name 
# return / tag_id
def create_tag(tag_name):
    access_token = get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/tags/create?access_token='+access_token
    data = {
        "tag": {
            "name": tag_name
        }
    }
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read() 
    tag_id = json.loads(result).get('tag').get('id')
    return tag_id


# 关注的用户打标签
# 参数 openid / tagid
def mob_create_tag(openid,tagid):
    access_token = get_token()
    url = 'https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token='+access_token
    data = {   
        "openid_list" : [openid],   
        "tagid" : tagid
    }
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    return 'ok'
    

# 获取用户是否存在标签
def del_tags(request):
    access_token = get_token()
    id = request.GET.get('id')
    url = 'https://api.weixin.qq.com/cgi-bin/tags/delete?access_token='+access_token
    data = {
        "tag":{
            "id" : id
        }
    }
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data,ensure_ascii=False).encode('utf8'))
    result = response.read()
    return HttpResponse("Hello World")



