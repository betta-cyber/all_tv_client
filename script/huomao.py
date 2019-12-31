#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import hashlib
import re


def get_time():
    tt = str(int((time.time() * 1000)))
    return tt


def get_videoids(rid):
    room_url = 'https://www.huomao.com/mobile/mob_live/' + str(rid)
    response = requests.get(url=room_url).text
    try:
        videoids = re.findall(r'var stream = "([\w\W]+?)";', response)[0]
    except Exception as e:
        videoids = 0
    return videoids


def get_token(videoids, time):
    token = hashlib.md5((str(videoids) + 'huomaoh5room' + str(time) +
                         '6FE26D855E1AEAE090E243EB1AF73685').encode('utf-8')).hexdigest()
    return token


def get_real_url(rid):
    videoids = get_videoids(rid)
    if videoids:
        time = get_time()
        token = get_token(videoids, time)
        room_url = 'https://www.huomao.com/swf/live_data'
        post_data = {
            'cdns': 1,
            'streamtype': 'live',
            'VideoIDS': videoids,
            'from': 'huomaoh5room',
            'time': time,
            'token': token
        }
        response = requests.post(url=room_url, data=post_data).json()
        roomStatus = response.get('roomStatus', 0)
        if roomStatus == '1':
            real_url = response.get('streamList')[0].get('list')[0]
        else:
            real_url = '直播间未开播'
    else:
        real_url = '直播间不存在'
    return real_url


rid = input('请输入火猫直播房间号：\n')
# set proxy
# import socket
# import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 8888)
# socket.socket = socks.socksocket
real_url = get_real_url(rid)
print('该直播间源地址为：\n')
print(real_url)
