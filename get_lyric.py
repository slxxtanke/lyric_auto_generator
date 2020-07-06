# -*- coding: utf-8 -*-
"""
@Author  : tanke
@Time    : 2020/7/1 15:51
"""

import os
import requests
import json
from requests.adapters import HTTPAdapter
import time
import sys
import threading
import math
from threading import Thread
import opencc
import base64
from html.parser import HTMLParser
import html
import taglib

import os

lrc_suffix = "lrc"


def lrc_QQ(title, artist):
    song_name = str(title.encode('utf-8'))
    song_name = song_name.replace('\\x', '%')[:-1]
    song_name = song_name[2:]

    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=15&w=' + song_name

    res = requests.get(url)
    response = json.loads(res.text.replace('callback(', '')[:-1])['data']['song']['list']
    song_ns = []
    singer_li = []
    for index, i in enumerate(response):
        singer_n = []
        for x in i['singer']:
            singer_n.append(x['name'])
        song_ns.append((index, '歌名： {}\n'.format(i['songname']) + '歌手： ' + '  &  '.join(singer_n) + '\n'))

    out = -1

    for index, i in enumerate(song_ns):
        print("{}: {}".format(index+1, i[1]))
    choice = int(input('请输入歌曲编号，不是输入0:  ')) - 1
    if 0 <= choice < len(i):
        out = choice
    else:
        return None
    mid = response[out]['songmid']
    for i in response[out]['singer']:
        singer_li.append(i['name'])
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg?nobase64=1&musicid={}&-=jsonp1&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(
        response[out]['songid'])
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://y.qq.com',
        'Referer': 'https://y.qq.com/n/yqq/song/' + mid + '.html',
        # 'User-Agent':' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    res = requests.get(url, headers=headers)  #
    h = HTMLParser()
    return html.unescape(res.json()['lyric'])



def scan_dictionary(path):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            filename, type = os.path.splitext(file)
            if not os.path.exists("{}/{}.{}".format(path, filename, lrc_suffix)):
                song = taglib.File('{}/{}'.format(path, file))
                if 'TITLE' in song.tags and len(song.tags['TITLE']) > 0:
                    title = song.tags['TITLE'][0]
                else:
                    title = filename
                if 'ARTIST' in song.tags and len(song.tags['ARTIST']) > 0:
                    artist = song.tags['ARTIST'][0]
                else:
                    artist = ""
                content = lrc_QQ(title, artist)
                if content == None:
                    pass
                else:
                    with open('{}/{}.{}'.format(path, filename, lrc_suffix), 'w', encoding='utf-8') as f:
                        f.write(content)



if __name__ == "__main__":
    scan_dictionary("D:\\music")


# print('''
# 本工具目前支持网易云和QQ音乐歌词下载
# 更新请移步 https://github.com/gongxi-cn-ln-dl/QQmusic-Lrc_downloader
# 感谢使用！''')
# time.sleep(3)
# os.system('cls')
# cho = input('''
# 请选择播放器
# 1.网易云音乐
# 2.QQ音乐''')
# if cho == '1':
#     lrc_163(input('请输入歌名: '))
# elif cho == '2':
#     lrc_QQ(input('请输入歌名: '), 'song')
# else:
#     print('请重新输入！')