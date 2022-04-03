import json
import os
import sys
import time

import requests
from colorama import *
from dingtalkchatbot.chatbot import DingtalkChatbot
from pypushdeer import PushDeer

# 城市代码，查看README
citycode = 'xxx'
# 检查间隔时间，单位分钟
checktime = 10
# 钉钉WebHook地址
DWebHook = 'xxx'
Dsecret = 'xxx'  # 可选：创建机器人勾选“加签”选项时使用
# PushDeer秘钥
# https://github.com/easychen/pushdeer
PushDeerKey = 'xxx'
# ServerChan秘钥
# https://sct.ftqq.com/
ServerChanKey = 'xxx'

# 程序部分，非专业人士请勿更改
FirstRun = True
b2 = ''


def job():
    if check_data(citycode) is not True:
        print(Fore.RED + '[-]---------------城市代码不能为空，请输入地区代码，详情查看README---------------[-]' + time.ctime())
        sys.exit(0)
    try:
        print(Fore.GREEN + '输入的地区代码为: ' + citycode)
    except IndexError:
        print(Fore.RED + 'usage: python3 9jiainfo.py cd')
    try:
        command = 'curl -H "Host: wxapidg.bendibao.com" -H "content-type: application/json" -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001034) NetType/4G Language/zh_CN" -H "Referer: https://servicewechat.com/wx2efc0705600eb6db/130/page-frame.html" --compressed "https://wxapidg.bendibao.com/smartprogram/zhuanti.php?platform=wx&version=21.12.06&action=jiujia&citycode={}"'.format(
            citycode)
    except UnboundLocalError:
        print(Fore.RED + '请输入地区代码，详情查看README')
    try:
        print(Fore.GREEN + '执行curl命令为:\n' + command)
        global FirstRun, b2
        if FirstRun is True:
            a1 = os.popen(command)
            b1 = a1.read()
            print(Fore.GREEN + '[+]---------------初始化请求完毕--------------[+]' + time.ctime())
            b2 = b1
        else:
            b1 = b2
            print(Fore.GREEN + '[+]---------------再次请求完毕---------------[+]' + time.ctime())
            a2 = os.popen(command)
            b2 = a2.read()
            b2 = b2
        print(Fore.GREEN + '[+]---------------间隔时间后的下一次请求完毕，进行内容比较---------------[+]' + time.ctime())
        r = json.loads(b2)
        data = r['data']
        jiujia = data['website']
        place = jiujia['place']
        try:
            global c
            c = ''
            for i in range(0, 5):
                c0 = '[+]---预约(抢)时间---[+]' + place[i]['yy_time'] + ' ' + place[i]['name'] + '    ' + '[+]---数量---: ' + \
                     place[i]['minge'] + '   ' + place[i]['method'] + '---预约平台---[+]' + place[i]['platform']
                c += c0 + '\n'
        except IndexError:
            pass
        print(c)
        if FirstRun is True:
            print(Fore.GREEN + '[+]---------------第一次运行，将进行推送---------------[+]' + time.ctime())
            push()
            FirstRun = False
        else:
            if b2 not in b1:
                print(Fore.GREEN + '[+]---------------九价信息更新了，将进行推送---------------[+]' + time.ctime())
                push()
            if b2 in b1:
                c = '九价信息暂未更新'
                print(Fore.RED + '[-]---------------九价信息暂未更新，推送未更新---------------[-]' + time.ctime())
        time.sleep(checktime * 60)
    except UnboundLocalError:
        sys.exit(2)


def check_data(data):
    if data == '' or len(data) == 0 or data is None or data == 'xxx':
        return False
    return True


def push():
    if out():
        return
    print(Fore.GREEN + '[+]---------------推送开始---------------[+]' + time.ctime())
    if check_data(DWebHook):
        dingtalk()
    if check_data(PushDeerKey):
        pushDeer()
    if check_data(ServerChanKey):
        serverChan()
    print(Fore.GREEN + '[+]---------------推送结束---------------[+]' + time.ctime())


def dingtalk():
    # 初始化机器人小丁
    # xiaoding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
    xiaoding = DingtalkChatbot(DWebHook, secret=Dsecret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
    # xiaoding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
    # Text消息@所有人
    xiaoding.send_text(msg=c, is_at_all=True)


def pushDeer():
    pushdeer = PushDeer(pushkey=PushDeerKey)
    pushdeer.send_text("九价疫苗有新消息！", desp=c)


def serverChan():
    ServerChan = 'https://sctapi.ftqq.com/' + ServerChanKey + '.send'
    requests.get(ServerChan, params={'text': "九价疫苗有新消息！", 'desp': c})


def out():
    if int(time.strftime('%H', time.localtime())) < 8:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        return True
    elif int(time.strftime('%H', time.localtime())) > 21:
        print(Fore.RED + '[-]---------------休息时间，不进行推送---------------[-]' + time.ctime())
        return False


def runJb():
    out()
    job()

while True:
    job()