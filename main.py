import os
# import random
# import time
# import csv
# import imageio.v2 as imageio
import numpy as np
import requests
import datetime
import json
from bs4 import BeautifulSoup
import shutil
import sys
import io
import jieba
import jieba.analyse
import jieba.posseg as pseg
import wordcloud
from matplotlib import image as mpimg, pyplot as plt
from PIL import Image

import main

# coding: utf-8
# 注意：如果文件乱码记事本打开另存文件格式为ANSI。编码后会导致部分符号丢失，可以参照源json文件分析。Steam用户ID太长可能会丢失，这里建议用评论唯一ID查找。
# 注意：英文评论中的”,“也会被记作csv分隔符，在这里先不做改善了，只讨论简中繁中情况。
# 更多说明查看https://partner.steamgames.com/doc/store/getreviews
# 游戏基本信息是英文，因为请求网站后默认英文语言，要改中文需要cookie。
# 有年龄限制浏览的部分游戏会爬取失效，因为需要输入生日验证。比如：《底特律：变人》、《黎明杀机》等，需要cookie。
# 关于价格：有时候获取到的价格是dlc价格（尤其是在这个游戏打折的时候），这是因为selector的问题，打折的价格selector会变，待修正。
# 有的游戏因为标题里带了:和其他一些奇葩字符导致建不了文件夹，更多奇葩字符有待修补。
# 如果词云里有重复词语，可能是因为相同词语连续大量出现(刷评论)，可以人工清洗再分析词云。
# jieba的词性tag需要python3.7才能用，有时间重建一下。

# 全局参数
jsfile_name = ''
Is_updated = 'False'
is_ch = 0  # 是否一开始启用cookie（能获得中文基本信息）
cookie_str = r'_ga=GA1.2.2063324720.1677846916; browserid=3120474609224450543; sessionid=6a93ee105e361d0735ff4135; timezoneOffset=28800,0; OUTFOX_SEARCH_USER_ID_NCOO=1402550032.5667572; deep_dive_carousel_method=default; steamCountry=HK|19912a30945f79648adec37bccaff724; strResponsiveViewPrefs=touch; birthtime=882028801; lastagecheckage=14-0-1998; Steam_Language=schinese; _gid=GA1.2.449215173.1683065095; _gac_UA-33786258-1=1.1683065095.Cj0KCQjw6cKiBhD5ARIsAKXUdyYmGPm6UanUhPxqtSMX0WvR_-oZgmtF_OUsnkib_5edmmITjwXSR-gaAtW9EALw_wcB; _gac_UA-222097716-1=1.1683065095.Cj0KCQjw6cKiBhD5ARIsAKXUdyYmGPm6UanUhPxqtSMX0WvR_-oZgmtF_OUsnkib_5edmmITjwXSR-gaAtW9EALw_wcB; ak_bmsc=9E0FFFCE49BBA82F2F378DF686E5CFA2~000000000000000000000000000000~YAAQV1DGy0v8SMaHAQAAcGx/3hNWLahi5LW60aEyl5/oWUNWA1np0JCBdYksN8J3YK4Leo0+7jf+EYGOY0DdSq060IVeungzZVYlTeziq3kA9/276RppXL1siyNrF8DUO4jxpcTnI4l8wCSPW1Mg2QoH+EgPrzKl/4tLNT2OjUWk0mpyOeV56BKZNiZer6KsvzmStM55dkd+KAQ/EsDUcWl+FHDmX7LLQc2Rt3B6XJVS8EDrT08Mk/NxlGptpt6mWbex5mwOZ30Ofq9UtWChytEzNR86Yaf6fWmhkeT8SgjmvKRdYWOCd7DA95C6wDB6pixDiNv59HkH5N8UAp9kE2A7vf2m5WTJfxcZbYDYDGINH6EAbwyJ3EQjiyfngrZCrmx5vEotL2w=; deep_dive_carousel_focused_app=674930; ___rl__test__cookies=1683066630776; bm_sv=CA2276B893F6C64B5B5945EC8D95B178~YAAQfjArF0hVO86HAQAAr3mo3hMbqG4mvm/k01ggjLOPzAbysc01szRoFnmv03WsGXjqBKGclwg0lpsrlu1GlauWBJBUMDICJhT1L5C0k80MIjbuoVUgxkVqvyye4tUo05NT//rFi2f6uN2BWAlp8ASXGavYBHJqQ51HuMc1ZSWDqLn7yBkJQ8dykyeEiPGZC+hBTuNQ17e80yFNPCkgJeLMx3Cr4HZ/NYlJH1967YJo28HgNONGq6AJzT6Rt3camsLw8Kyo~1; _gat_app=1; app_impressions=1619210@1_7_7_151_150_1|1224230@1_7_7_151_150_1|1101870@1_7_7_151_150_1|721180@1_7_7_151_150_1|1209770@1_7_7_151_150_1|1311700@1_7_7_151_150_1|2150830@1_7_7_151_150_1|1323540@1_7_7_151_150_1|614582@1_7_7_151_150_1|1790370@1_7_7_151_150_1|606971@1_7_7_151_150_1|2095300@1_7_7_151_150_1|1222140@1_7_7_151_150_1|2218230@1_7_7_151_150_1|2263670@1_7_7_151_150_1|1236420@1_7_7_151_150_1|1607540@1_7_7_151_150_1|960910@1_5_9__412|960990@1_5_9__412|1222140@1_5_9__412|1774580@1_5_9__300_6|1091500@1_5_9__300_5|1174180@1_5_9__300_4|1888930@1_5_9__300_3|1057090@1_5_9__300_2|292030@1_5_9__300_1; recentapps={"292030":1683068083,"1222140":1683068055,"2150830":1683068041,"513710":1683065092,"2058190":1682894811,"1948280":1682894289,"381210":1682891334,"846470":1682890077,"322330":1682888070,"1687950":1682885222}'
game_name = ''
flag = 0
n2 = 0
cur_dir = "c:\\Users\\Lenovo\\Desktop"
flag_bytes = 0
proxies = {
    'http':'http://127.0.0.1:10809',
    'https':'http://127.0.0.1:10809'
}
trans_tag = {
    'n': '普通名词',
    'f': '方位名词',
    's': '处所名词',
    't': '时间',
    'nr': '人名',
    'ns': '地名',
    'nt': '机构名',
    'nw': '作品名',
    'nz': '其他专名',
    'v': '普通动词',
    'vd': '动副词',
    'vn': '名动词',
    'a': '形容词',
    'ad': '副形词',
    'an': '名形词',
    'd': '副词',
    'm': '数量词',
    'q': '量词',
    'r': '代词',
    'p': '介词',
    'c': '连词',
    'u': '助词',
    'xc': '其他虚词',
    'w': '标点符号',
    'PER': '人名',
    'LOC': '地名',
    'ORG': '机构名',
    'TIME': '时间',
}

trans_tag_group = {
    'n': '名词',
    'f': '时量地',
    's': '时量地',
    't': '时量地',
    'nr': '专名',
    'ns': '专名',
    'nt': '专名',
    'nw': '专名',
    'nz': '专名',
    'v': '动词',
    'vd': '动词',
    'vn': '动词',
    'a': '形容词',
    'ad': '形容词',
    'an': '形容词',
    'd': '形容词',
    'm': '时量地',
    'q': '时量地',
    'r': '其他',
    'p': '其他',
    'c': '其他',
    'u': '其他',
    'xc': '其他',
    'w': '其他',
    'PER': '专名',
    'LOC': '时量地',
    'ORG': '专名',
    'TIME': '时量地',
}

list_zhuanming = []
list_shiliangdi = []
list_dongci = []
list_xingrongci = []
list_mingci = []

params = {
    'json': 1,
    'filter': 'recent',
    # recent – 以创建时间排序；updated – 以最后更新时间排序；all – （默认）以值得参考的程度排序，基于 day_range 参数作为滑动窗口，总是找到可返回的结果。如果使用光标对评测进行翻页，可以选择“recent”选项或“updated”选项，直至最终收到的响应列表为空。
    'language': 'schinese,tchinese',
    # all来获得所有语言；schinese来获得简中语言,english来获得英文语言，tchinese获取繁中语言,更多参考https://partner.steamgames.com/doc/store/localization/languages
    'day_range': 365,  # 从现在至 N 天前，查找值得参考的评测。 仅适用于“all” 筛选器。 最大值为 365。
    'review_type': 'all',  # all – 所有评测（默认）；positive – 仅限正面评测；negative – 仅限负面评测
    'purchase_type': 'all',
    # all – 所有评测；non_steam_purchase – 在 Steam 上未付费获得产品的用户撰写的评测；steam – 在 Steam 上付费获得产品的用户撰写的评测（默认设置）
    'num_per_page': 100  # 默认情况下，最多可返回 20 条评测。 视此参数而定，可返回更多评测（最多 100 条）。
}
basic = {
    'name': 'Name',  # 游戏名
    'developer': 'Developer',  # 开发商
    'publisher': 'Publisher',  # 发行商
    'desc': 'Description',  # 游戏简介
    'date': 'Date',  # 发行日期
    'tags': '',  # 游戏标签
    'price': '',  # 价格
    'review_total': 'Review_total',  # 至今评测
    'review_recent': 'Review_recent',  # 近期评测
    'steam_feature': 'fun',  # 功能
    'achievement_num': 0,  # 成就数
    'support_languages': 'Language',  # 支持语言
    'Support_Sch': 'True'  # 支持中文
}

achievement = {
    'achievement_name': 'Name',  # 成就名
    'achievement_desc': 'Achievement_desc',  # 成就描述
    'achievement_percentage': 'Achievement_percentage'  # 全球达成比
}

achievement_list = []

# 停用词列表(筛选词云生成)
stopwords = ['还是', '是', '一种', '等', '游戏', '就是', '一个', '这样', 'sb', '骚逼', '头像', '点数', 'Steam点数',
             'Steam 点数',
             '牛子', '如果', '觉得', '什么', '一下', '这个', '遊戯', 'game', 'really', 'now', 'right', 'the', 'and',
             'it', 'so', 'to', 'you', 'of', 'this', 'in', 'on', 'that', 'there', 'for', 'are', 'as', 'was', 'at',
             'This', 'just', 'an', 'way', 'will', 'games', 'play', 'playing', 'https', 'url', 'tmd', 'h1', '可以']
# WorldCloud自带stopword功能。
stopwords_set = wordcloud.STOPWORDS
stopwords_set.update(stopwords)

# 屏蔽词列表(筛选无效评论)
filterwords = ['牛子', 'steam点数', 'Steam 点数', '请奖励这条评论', '点赞这条评论', '买那些骚逼头像和背景', '给我点赞',
               '一赞摸一次',
               '一个赞摸一次', '路过的朋友', '你好,陌生人', '可以过来摸一摸', '這裡養了一隻', '这里养了一只']


def word_cloud(img, commentcloud):
    global is_ch
    global jsfile_name
    global list_xingrongci
    global list_zhuanming
    global list_shiliangdi
    global list_dongci
    global list_mingci
    pic = img
    sentence = '.'.join(commentcloud).replace('，', ',')
    sentence = sentence.replace('。', '.')
    sentence = sentence.replace('：', ':')
    sentence = sentence.replace('“', '"')
    sentence = sentence.replace('”', '"')
    sentence = sentence.replace('  ', '')
    jieba.enable_paddle()
    seg_list = jieba.cut('.'.join(commentcloud), cut_all=False, use_paddle=True)  # 精确模式
    seg_list_tag = pseg.cut(sentence, use_paddle=True)
    # print(seg_list_tag)
    for word, flag in seg_list_tag:
        #if flag != 'w' and len(word) > 1:
            #print('%s %s' % (word, trans_tag[flag]))
        if  len(word) > 1 and word not in stopwords:
            if trans_tag_group[flag] == '时量地':
                list_shiliangdi.append(word.replace(' ',''))
                #print('%s' % word)
            elif trans_tag_group[flag] == '专名':
                list_zhuanming.append(word.replace(' ',''))

            elif trans_tag_group[flag] == '名词':
                list_mingci.append(word.replace(' ', ''))

            elif trans_tag_group[flag] == '动词':
                list_dongci.append(word.replace(' ',''))

            elif trans_tag_group[flag] == '形容词':
                list_xingrongci.append(word.replace(' ',''))
    shiliangdi = ' '.join(list_shiliangdi)
    zhuanming = ' '.join(list_zhuanming)
    dongci = ' '.join(list_dongci)
    xingrongci = ' '.join(list_xingrongci)
    mingci = ' '.join(list_mingci)
    words_filtered = [word for word in seg_list if word not in stopwords and len(word) > 1]
    # print(words_filtered)
    words = ' '.join(words_filtered)
    # print(words)
    word_count = {}
    for word in words_filtered:
        if len(word) > 1:
            word_count[word] = word_count.get(word, 0) + 1
    output = 'word,count'
    for word, count in word_count.items():
        output += '\n' + word + ',' + str(count)
    if is_ch == '4':
        with open(jsfile_name + '-wordcloud_post2.csv', 'w', encoding='gbk') as f:
            output = output.encode('gbk', "ignore")
            output = output.decode('gbk', "ignore")
            f.write(output)
        print("Wordcloud后处理已完成，请查看" + jsfile_name + '-wordcloud_post2.csv CSV文件')
    else:
        with open(game_name + '-' + AppID + '-wordcloud_post.csv', 'w', encoding='gbk') as f:
            output = output.encode('gbk', "ignore")
            output = output.decode('gbk', "ignore")
            f.write(output)
        print("Wordcloud后处理已完成，请查看" + game_name + '-' + AppID + '-wordcloud_post.csv CSV文件')
    # print(word, count)
    # 保存
    wc = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                             width=1000, height=500,
                             background_color='white').generate(words)
    wc_adj = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                             width=1000, height=500,
                             background_color='white').generate(xingrongci)
    wc_zn = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                                 width=1000, height=500,
                                 background_color='white').generate(zhuanming)
    wc_n = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                               width=1000, height=500,
                               background_color='white').generate(mingci)
    wc_v = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                               width=1000, height=500,
                               background_color='white').generate(dongci)
    wc_t = wordcloud.WordCloud(mask=pic, font_path='C:\\Users\\Lenovo\\PycharmProjects\\pySteam\\STZHONGS.TTF',
                               width=1000, height=500,
                               background_color='white').generate(shiliangdi)
    # print(words)
    wc.to_file('wordcloud.png')
    print("Wordcloud已保存")
    wc_adj.to_file('wordcloud_adj.png')
    print("形容词Wordcloud已保存")
    wc_v.to_file('wordcloud_v.png')
    print("动词Wordcloud已保存")
    wc_n.to_file('wordcloud_n.png')
    print("名词Wordcloud已保存")
    wc_zn.to_file('wordcloud_zn.png')
    print("专名Wordcloud已保存")
    wc_t.to_file('wordcloud_t.png')
    print("状语Wordcloud已保存")
    # print(word_count)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    # plt.savefig('wordcloud2.png', dpi=300)  # 指定分辨率保存


def get_game_achieve_cookie(appid):
    global cookie_str
    url = "https://steamcommunity.com/stats/%s/achievements" % appid
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    url = url
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'User-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'}
    r = requests.get(url=url, headers=headers, cookies=cookies, proxies=proxies)
    html = r.content.decode('utf-8', 'ignore')
    page2 = BeautifulSoup(html, 'lxml')
    for tag in page2.select('#view_product_page_btn > span'):
        if tag.get_text() == 'View Page' or '查看页面':
            cookie_str = input(
                'Cookie已失效，请于Steam网页登录->右键检查->网络(全部)->(刷新后)任意项->复制cookie重新粘贴于此处：')
            get_game_achieve_cookie(appid)
    game_achieve_num = 0
    p = 0
    for tag in page2.select('#headerContentLeft > span:nth-child(1)'):
        basic['achievement_num'] = int(tag.get_text())
        game_achieve_num = basic['achievement_num']

    while p <= game_achieve_num + 3:
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achieveTxt > h3' % p):
            achievement['achievement_name'] = tag.get_text()
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achieveTxt > h5' % p):
            achievement['achievement_desc'] = tag.get_text()
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achievePercent' % p):
            achievement['achievement_percentage'] = tag.get_text()
            achievement_list.append(achievement.copy())  # 直接append会导致列表元素直接指向原字典，一改全改
        p = p + 1
    # print(achievement_list)
    output3 = 'index,'
    index = 1
    output3 += ','.join(achievement)
    for a in achievement_list:
        output3 += '\n'
        output3 += str(index) + ','
        for b in a.values():
            if ',' in str(b):
                output3 += f'{b}'.replace(',', '，') + ','
            else:
                output3 += f'{b},'
        index = index + 1
        # 将结果写到到csv中
    with open(game_name + '-' + AppID + '-achievements_post.csv', 'w', encoding='gbk') as f:
        output3 = output3.encode('gbk', "ignore")
        output3 = output3.decode('gbk', "ignore")
        f.write(output3)
    print("Achievements后处理已完成，请查看" + game_name + '-' + AppID + '-achievements_post.csv CSV文件')


def get_game_achieve(appid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'}
    url = "https://steamcommunity.com/stats/%s/achievements" % appid
    r = requests.get(url=url, headers=headers, proxies=proxies)
    html = r.content.decode('utf-8', 'ignore')
    page2 = BeautifulSoup(html, 'lxml')
    game_achieve_num = 0
    p = 0
    for tag in page2.select('#headerContentLeft > span:nth-child(1)'):
        basic['achievement_num'] = int(tag.get_text())
        game_achieve_num = basic['achievement_num']

    while p <= game_achieve_num + 3:
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achieveTxt > h3' % p):
            achievement['achievement_name'] = tag.get_text()
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achieveTxt > h5' % p):
            achievement['achievement_desc'] = tag.get_text()
        for tag in page2.select('#mainContents > div:nth-child(%d) > div.achieveTxtHolder > div.achievePercent' % p):
            achievement['achievement_percentage'] = tag.get_text()
            achievement_list.append(achievement.copy())  # 直接append会导致列表元素直接指向原字典，一改全改
        p = p + 1
    # print(achievement_list)
    output3 = 'index,'
    index = 1
    output3 += ','.join(achievement)
    for a in achievement_list:
        output3 += '\n'
        output3 += str(index) + ','
        for b in a.values():
            if ',' in str(b):
                output3 += f'{b}'.replace(',', '，') + ','
            else:
                output3 += f'{b},'
        index = index + 1
        # 将结果写到到csv中
    with open(game_name + '-' + AppID + '-achievements_post.csv', 'w', encoding='utf8') as f:
        f.write(output3)
    print("Achievements后处理已完成，请查看" + game_name + '-' + AppID + '-achievements_post.csv CSV文件')


def auto_login(url, cookie_str):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    url = url
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    html = r.content.decode('utf-8', 'ignore')
    # html.replace('en', 'zh-cn')
    page = BeautifulSoup(html, 'lxml')
    # print(page.prettify())

    for tag in page.select('#view_product_page_btn > span'):
        if tag.get_text() == 'View Page':
            cookie = input(
                'Cookie已失效，请于Steam网页登录->右键检查->网络(全部)->(刷新后)任意项->复制cookie重新粘贴于此处：')
            auto_login(url, cookie)
    return page


def get_basic_gameinfo(appid):
    global is_ch
    global game_name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36'}
    url = "https://store.steampowered.com/app/"
    r = requests.get(url=url + str(appid), headers=headers, proxies=proxies)
    html = r.content.decode('utf-8', 'ignore')
    # html.replace('en', 'zh-cn')
    page = BeautifulSoup(html, 'lxml')
    # print(page.prettify())

    for tag in page.select('#view_product_page_btn > span'):
        if tag.get_text() == 'View Page' or is_ch == 1:
            page = auto_login(url + str(appid) + '_/', cookie_str)
            is_ch = 1
            # exit()

    for tag in page.find_all('div', class_='apphub_AppName', id='appHubAppName'):
        basic['name'] = tag.get_text()
    if ':' in str(basic['name']):
        game_name = basic['name'].replace(':', '：')
    else:
        game_name = basic['name']
    folder_name = game_name + '-' + AppID
    # os.chdir(cur_dir)
    # os.mkdir(os.path.join(cur_dir, folder_name))
    if os.path.exists(folder_name):
        print("文件夹已存在")
    else:
        os.mkdir(folder_name)
    os.chdir(folder_name)
    print("源网页已获取，请查看" + game_name + '-' + AppID + '-summary.html HTML源文件')
    with open(game_name + '-' + AppID + '-summary.html', 'w', encoding='utf8') as f:
        f.write(html)

    for tag in page.select('#developers_list > a'):
        basic['developer'] = tag.get_text()

    for tag in page.select(
            '#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a'):
        basic['publisher'] = tag.get_text()

    for tag in page.select('#game_highlights > div.rightcol > div > div.game_description_snippet'):
        basic['desc'] = tag.get_text()
    basic['desc'] = basic['desc'].replace('\t', '')
    basic['desc'] = basic['desc'].replace('\r\n', '')
    basic['desc'] = basic['desc'].replace(',', '，')

    for tag in page.select(
            '#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div.release_date > div.date'):
        basic['date'] = tag.get_text()
        basic['date'] = basic['date'].replace(',', '/')

    for tag in page.find_all('div', class_='game_purchase_price price'):
        basic['price'] = tag.get_text()
        basic['price'] = basic['price'].replace(',', '.')
        basic['price'] = basic['price'].replace('\r\n', '')
        basic['price'] = basic['price'].replace('\t', '')
    # game_area_purchase_section_add_to_cart_%s > div.game_purchase_action > div > div.game_purchase_price.price
    # game_area_purchase_section_add_to_cart_735326 > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_original_price

    for tag in page.select(
            '#userReviews > div:nth-child(1) > div.summary.column > span.nonresponsive_hidden.responsive_reviewdesc'):
        basic['review_recent'] = tag.get_text()
    basic['review_recent'] = basic['review_recent'].replace('\t- ', '')
    basic['review_recent'] = basic['review_recent'].replace('\r\n', '')
    basic['review_recent'] = basic['review_recent'].replace('\t', '')
    basic['review_recent'] = basic['review_recent'].replace(',', '')

    for tag in page.select(
            '#userReviews > div:nth-child(2) > div.summary.column > span.nonresponsive_hidden.responsive_reviewdesc'):
        basic['review_total'] = tag.get_text()
    basic['review_total'] = basic['review_total'].replace('\t- ', '')
    basic['review_total'] = basic['review_total'].replace('\t', '')
    basic['review_total'] = basic['review_total'].replace('\r\n', '')
    basic['review_total'] = basic['review_total'].replace(',', '')

    tag_list = []
    for tag in page.find_all('a', class_='app_tag'):
        # print(tag)
        tag_temp = tag.get_text().replace('\r\n', '')
        tag_temp = tag_temp.replace('\t', '')
        tag_list.append(tag_temp)
    # print(tag_list)
    basic['tags'] = ";".join(tag_list)
    # for a in tag_list:
    # print(a)

    ## Steam 功能
    for tag in page.select('#category_block > div > a:nth-child(1) > div.label'):
        basic['steam_feature'] = tag.get_text()
    for i in range(18):
        i = i + 2
        for tag in page.select('#category_block > div > a:nth-child(%d) > div.label' % i):
            basic['steam_feature'] += ';' + tag.get_text()

    ## 支持语言
    str1 = ''
    list = page.find_all('td', class_='ellipsis')
    leng = len(list)
    basic['language_num'] = leng
    for tag in list:
        # print(tag)
        str1 += tag.get_text() + ';'
    str1 = str1.replace(';\r\n\t\t\t\t', ';')
    str1 = str1.replace('\t\t\t;', ';')
    str1 = str1[6:len(str1) - 1]
    basic['support_languages'] = str1

    ## 支持中文
    for tag in page.select('#languageTable > table > tbody > tr.unsupported > td.ellipsis'):
        if tag.get_text() == 'Simplified Chinese':
            basic['Support_Sch'] = 'False'
        else:
            basic['Support_Sch'] = 'True'

    return game_name

    # print(basic)


def post_process():
    # with Python中的上下文管理器，会帮我们释放资源，比如 关闭文件句柄
    # open 函数为Python内建的文件读取函数，r代表只读

    ## Summary后期处理
    with open(game_name + '-' + AppID + '-summary.json', 'r', encoding='utf8') as f:
        # 解析一个有效的JSON字符串并将其转换为Python字典
        data = json.loads(f.read())
    output = ','.join(basic)
    output += ','
    output += ','.join([*data[0]])
    output += ','
    params_output = params
    del params_output['json']
    del params_output['num_per_page']
    del params_output['cursor']
    output += ','.join(params_output)
    # 遍历 字典列表data
    output += '\n'
    for obj2 in basic:
        output += f'{basic[obj2]},'
    for obj in data:
        # 将结果转化为字符串，累加到output中
        # f 为f-string格式化，将大括号中的表达式替代
        output += f'%s,{obj["review_score"]},{obj["review_score_desc"]},{obj["total_positive"]},{obj["total_negative"]},{obj["total_reviews"]}' % str(
            n - n2)
    for key in params_output:
        if ',' in str(params_output[key]):
            output += ',' + f'{params_output[key]}'.replace(',', '/')
        else:
            output += f',{params_output[key]}'
    # 将结果写到到csv中
    with open(game_name + '-' + AppID + '-summary_post.csv', 'w', encoding='gbk') as f:
        output = output.encode('gbk', 'replace')
        output = output.decode('gbk', 'replace')
        f.write(output)
    print("Summary后处理已完成，请查看" + game_name + '-' + AppID + '-summary_post.csv CSV文件')

    ## Reviews后期处理
    sus_count = 0
    commentcloud = []
    with open(game_name + '-' + AppID + '-reviews.json', 'r', encoding='utf8') as f:
        # 解析一个有效的JSON字符串并将其转换为Python字典
        data = f.read().replace('],[', ',')
        data = data.replace('\\n', ';')
        data = data.replace('\n,', ',')
        data = data.replace('%', '%%')
    with open(game_name + '-' + AppID + '-reviews.json', 'w', encoding='utf8') as f:
        f.write(data)
    # 使用 ，连接列表中的值
    # data[0]是一个字典类型，一个星号代表展开键，两个星号（**）代表展开字典的值
    with open(game_name + '-' + AppID + '-reviews.json', 'r', encoding='utf8') as f:
        # 解析一个有效的JSON字符串并将其转换为Python字典
        data = json.loads(f.read())
    author_data_title = [*data[0]['author']]
    output2 = ','.join(author_data_title)
    output2 += ','.join([*data[0]])
    output2 += ',review_length'
    output2 += ',review_updated'  # 评论是否更新过
    output2 += ",timestamp_dev_responded, developer_response"
    output2 = output2.replace('author,', '')
    output2 = output2.replace('recommendationid', ',recommendationid')
    output2 = output2.replace('playtime_forever', 'playtime_forever(min)')
    output2 = output2.replace('playtime_last_two_weeks', 'playtime_last_two_weeks(min)')
    output2 = output2.replace('playtime_at_review', 'playtime_at_review(min)')
    output_sus = output2  # 可疑的无效评论单独放在一个文件里
    # 遍历 字典列表data
    for obj in data:
        review_len = len(obj["review"])
        author_data = [obj['author']]
        timestamp_created = readable_unixtime(obj["timestamp_created"])
        timestamp_updated = readable_unixtime(obj["timestamp_updated"])
        if "timestamp_dev_responded" in obj:
            timestamp_dev_responded = readable_unixtime(obj["timestamp_dev_responded"])
        else:
            timestamp_dev_responded = ''
        if "developer_response" in obj:
            developer_response = str(obj["developer_response"]).replace(',', '，')
        else:
            developer_response = ''
        if timestamp_created == timestamp_updated:
            Is_updated = 'False'
        else:
            Is_updated = 'True'
        Is_in = 0
        for w in filterwords:
            if w in obj["review"]:
                Is_in = 1
                break  # 这里要break是因为循环是按照filterwords列表的个数为参考的，如果不break就意味着每次匹配条件后都append一遍当前的review
        if Is_in == 0:
            commentcloud.append(obj["review"])
            output2 += f'\n'
            # 将结果转化为字符串，累加到output中
            for obj2 in author_data:
                last_played = readable_unixtime(obj2["last_played"])
                output2 += f'{obj2["steamid"]},{obj2["num_games_owned"]},{obj2["num_reviews"]},{obj2["playtime_forever"]},{obj2["playtime_last_two_weeks"]},{obj2["playtime_at_review"]},%s' % str(
                    last_played)
            review_fix = str(obj["review"]).replace(',', '，')
            # f 为f-string格式化，将大括号中的表达式替代
            output2 += f',{obj["recommendationid"]},{obj["language"]},{review_fix},%s,%s,{obj["voted_up"]},{obj["votes_up"]},{obj["votes_funny"]},{obj["weighted_vote_score"]},{obj["comment_count"]},{obj["steam_purchase"]},{obj["received_for_free"]},{obj["written_during_early_access"]},{obj["hidden_in_steam_china"]},{obj["steam_china_location"]},{review_len},{Is_updated},{timestamp_dev_responded},{developer_response}' % (
                str(timestamp_created), str(timestamp_updated))
        else:
            print("已过滤无效评论:" + obj["review"])
            output_sus += f'\n'
            sus_count = sus_count + 1
            # 将结果转化为字符串，累加到output中
            for obj2 in author_data:
                last_played = readable_unixtime(obj2["last_played"])
                output_sus += f'{obj2["steamid"]},{obj2["num_games_owned"]},{obj2["num_reviews"]},{obj2["playtime_forever"]},{obj2["playtime_last_two_weeks"]},{obj2["playtime_at_review"]},%s' % str(
                    last_played)
            review_fix = str(obj["review"]).replace(',', '，')
            # f 为f-string格式化，将大括号中的表达式替代
            output_sus += f',{obj["recommendationid"]},{obj["language"]},{review_fix},%s,%s,{obj["voted_up"]},{obj["votes_up"]},{obj["votes_funny"]},{obj["weighted_vote_score"]},{obj["comment_count"]},{obj["steam_purchase"]},{obj["received_for_free"]},{obj["written_during_early_access"]},{obj["hidden_in_steam_china"]},{obj["steam_china_location"]},{review_len},{Is_updated}' % (
                str(timestamp_created), str(timestamp_updated))
    # 将结果写到到output.csv中
    # 游玩时间单位是分钟
    if sus_count == 0:
        print('恭喜!游戏大概是小众到没有可疑评论呢！')
    else:
        with open(game_name + '-' + AppID + '-reviews_sus_post.csv', 'w', encoding='gbk') as f:
            output_sus = output_sus.encode('gbk', "ignore")
            output_sus = output_sus.decode('gbk', "ignore")
            f.write(output_sus)
        print(
            str(sus_count) + "条可疑无效Reviews已隔离，请查看" + game_name + '-' + AppID + '-reviews_sus_post.csv CSV文件')
    with open(game_name + '-' + AppID + '-reviews_post.csv', 'w', encoding='gbk') as f:
        output2 = output2.encode('gbk', "ignore")
        output2 = output2.decode('gbk', "ignore")
        f.write(output2)
    print("Reviews后处理已完成，请查看" + game_name + '-' + AppID + '-reviews_post.csv CSV文件')

    doc_name = game_name + '-' + AppID
    if os.path.exists('source'):
        shutil.rmtree('source')
        os.mkdir('source')
    else:
        os.mkdir('source')
    if os.path.exists(doc_name + "-summary.html"):
        shutil.move(doc_name + "-summary.html", "source")
    shutil.move(doc_name + "-reviews.json", "source")
    shutil.move(doc_name + "-summary.json", "source")

    return commentcloud


# 函数：Unix时间戳可读化
def readable_unixtime(unix_timestamp):
    # Define a Unix timestamp
    unix_timestamp = unix_timestamp
    # Convert the Unix timestamp to a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
    # Convert the datetime object to a human-readable string
    readable_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    return readable_time


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。
    try:
        r = requests.get(url='https://store.steampowered.com/appreviews/718670?json=1', timeout=8, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
        if str(r.status_code) == '200':
            print('评论获取网络已连通！(1/3)')
            r = requests.get(url='https://steamcommunity.com/stats/718670/achievements', timeout=8, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
            if str(r.status_code) == '200':
                print('成就获取网络已连通！(2/3)')
                r = requests.get(url='https://store.steampowered.com/app/718670/Cultist_Simulator/', timeout=8,
                                 headers={
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
                if str(r.status_code) == '200':
                    print('基本信息获取网络已连通！(3/3)')
                else:
                    print('基本信息网络无法连通！请尝试重载request包、重启项目或关闭/打开代理')
            else:
                print('成就获取网络无法连通！请尝试重载request包、重启项目或关闭/打开代理')
        else:
            print('评论获取网络无法连通！请尝试重载request包、重启项目或关闭/打开代理')

    except Exception as e:
        print('网络无法连通！请尝试重载request包、重启项目或关闭/打开代理')
        print(e)
        print("程序已结束")
        exit()


def get_reviews(appid, params):
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(appid) + '?json=1', params=params, headers={'User-Agent': 'Mozilla/5.0'}, proxies=proxies)
    return response.json()


def get_n_reviews(appid, n2, n, cursor="*"):
    summary = []
    reviews = []

    while n > 0:
        # print(type(cursor))
        # if not type(cursor) == "<class 'bytes'>":
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n2)
        n2 = n2 - params['num_per_page']
        response = get_reviews(appid, params)
        cursor = response['cursor']
        code = response['success']
        params['cursor'] = cursor
        if code == 1:
            print("Success!\nNext cursor:" + cursor)
            reviews += response['reviews']
            summary = response['query_summary']
            break

        # 开启上条代码以限制获取评论数量
    print("已获取" + str(len(response['reviews'])) + "条评论")
    print(game_name + '-' + AppID + "-reviews.json 已更新")
    # print(reviews)
    data = reviews  # 评论
    if flag == 0:
        # print(summary)
        data2 = summary  # 游戏数据
        print(game_name + '-' + AppID + "-summary.json 已更新")
        with open(game_name + '-' + AppID + '-reviews.json', 'w', encoding='utf8') as f2:
            # ensure_ascii=False才能输入中文，否则是Unicode字符
            # indent=2 JSON数据的缩进，美观
            json.dump(data, f2, ensure_ascii=False, indent=2)
        with open(game_name + '-' + AppID + '-summary.json', 'w', encoding='utf8') as f2:
            f2.write("[")
            json.dump(data2, f2, ensure_ascii=False, indent=2)
            f2.write("]")
        with open(game_name + '-' + AppID + '-summary.json', 'r', encoding='utf8') as f:
            # 解析一个有效的JSON字符串并将其转换为Python字典
            data = json.loads(f.read())
        for obj in data:
            if obj["total_reviews"] < n:
                # print(obj["total_reviews"])
                print("符合条件的评论总数小于请求数(" + str(n) + "/" + str(obj["total_reviews"]) + ")！")
                # global n # 调用全局变量需要声明global
                main.n = int(obj["total_reviews"])
                n2 = int(obj["total_reviews"]) - params['num_per_page']
    else:
        with open(game_name + '-' + AppID + '-reviews.json', 'a', encoding='utf8') as f2:
            # ensure_ascii=False才能输入中文，否则是Unicode字符
            # indent=2 JSON数据的缩进，美观
            f2.write(",")  # 统一格式的时候将“],[”用“,”替换
            json.dump(data, f2, ensure_ascii=False, indent=2)
    if cursor == '*':
        print("没有查询到这个游戏！")
        exit()
    return n2


def transform_mask(img):
    # 这里使用的jpg，文件后缀根据自己情况改哦！
    img = img[:, :, 0]  # transform 3d image to 2d for easier visualization

    def transform_format(val):
        if val.any() == 0:
            return 255
        else:
            return val


def skip_cookie():
    global game_name
    global n
    game_name = 'Game'
    n = int(input("请输入获取数量:"))
    folder_name = game_name + '-' + AppID
    if os.path.exists(folder_name):
        print("文件夹已存在")
    else:
        os.mkdir(folder_name)
    os.chdir(folder_name)
    n2 = n
    flag = 0
    n2 = get_n_reviews(AppID, n2, n)
    flag = 1
    # flag_bytes = 1
    # readable_unixtime(1680409828)
    if not n2 == 0:
        Cursor = input("请回车以获取下一批评论（剩余%d条）,输入0以结束:" % n2)
        while Cursor is not None:
            try:
                n2 = get_n_reviews(AppID, n2, n, params['cursor'])
                Cursor = '*'
                if not n2 == 0:
                    Cursor = input("请回车以获取下一批评论（剩余%d条）,输入0以结束:" % n2)
                    if Cursor == "0" or Cursor == "*" or Cursor == '\n' or n2 == 0:
                        break
                else:
                    break
            except Exception as e:
                commentcloud = post_process()
                word_cloud(img, commentcloud)
                print(e)
                print("程序已结束")
                exit()
    else:
        commentcloud = post_process()
        word_cloud(img, commentcloud)
        exit()

    commentcloud = post_process()
    word_cloud(img, commentcloud)
    exit()


def word_cloud_process(jsfile):
    global jsfile_name
    sus_count = 0
    commentcloud = []
    # 使用 ，连接列表中的值
    # data[0]是一个字典类型，一个星号代表展开键，两个星号（**）代表展开字典的值
    if os.path.exists(jsfile_name):
        print("文件夹已存在")
    else:
        os.mkdir(jsfile_name)
    if os.path.exists(jsfile):
        shutil.move(jsfile, jsfile_name)
    os.chdir(jsfile_name)
    with open(jsfile, 'r', encoding='utf8') as f:
        # 解析一个有效的JSON字符串并将其转换为Python字典
        data = json.loads(f.read())

    author_data_title = [*data[0]['author']]
    output2 = ','.join(author_data_title)
    output2 += ','.join([*data[0]])
    output2 += ',review_length'
    output2 += ',review_updated'  # 评论是否更新过
    output2 += ",timestamp_dev_responded, developer_response"
    output2 = output2.replace('author,', '')
    output2 = output2.replace('recommendationid', ',recommendationid')
    output2 = output2.replace('playtime_forever', 'playtime_forever(min)')
    output2 = output2.replace('playtime_last_two_weeks', 'playtime_last_two_weeks(min)')
    output2 = output2.replace('playtime_at_review', 'playtime_at_review(min)')
    output_sus = output2  # 可疑的无效评论单独放在一个文件里
    # 遍历 字典列表data
    for obj in data:
        review_len = len(obj["review"])
        author_data = [obj['author']]
        timestamp_created = readable_unixtime(obj["timestamp_created"])
        timestamp_updated = readable_unixtime(obj["timestamp_updated"])
        if "timestamp_dev_responded" in obj:
            timestamp_dev_responded = readable_unixtime(obj["timestamp_dev_responded"])
        else:
            timestamp_dev_responded = ''
        if "developer_response" in obj:
            developer_response = str(obj["developer_response"]).replace(',', '，')
        else:
            developer_response = ''
        if timestamp_created == timestamp_updated:
            Is_updated = 'False'
        else:
            Is_updated = 'True'
        Is_in = 0
        for w in filterwords:
            if w in obj["review"]:
                Is_in = 1
                break  # 这里要break是因为循环是按照filterwords列表的个数为参考的，如果不break就意味着每次匹配条件后都append一遍当前的review
        if Is_in == 0:
            commentcloud.append(obj["review"])
            output2 += f'\n'
            # 将结果转化为字符串，累加到output中
            for obj2 in author_data:
                last_played = readable_unixtime(obj2["last_played"])
                output2 += f'{obj2["steamid"]},{obj2["num_games_owned"]},{obj2["num_reviews"]},{obj2["playtime_forever"]},{obj2["playtime_last_two_weeks"]},{obj2["playtime_at_review"]},%s' % str(
                    last_played)
            review_fix = str(obj["review"]).replace(',', '，')
            # f 为f-string格式化，将大括号中的表达式替代
            output2 += f',{obj["recommendationid"]},{obj["language"]},{review_fix},%s,%s,{obj["voted_up"]},{obj["votes_up"]},{obj["votes_funny"]},{obj["weighted_vote_score"]},{obj["comment_count"]},{obj["steam_purchase"]},{obj["received_for_free"]},{obj["written_during_early_access"]},{obj["hidden_in_steam_china"]},{obj["steam_china_location"]},{review_len},{Is_updated},{timestamp_dev_responded},{developer_response}' % (
                str(timestamp_created), str(timestamp_updated))
        else:
            print("已过滤无效评论:" + obj["review"])
            output_sus += f'\n'
            sus_count = sus_count + 1
            # 将结果转化为字符串，累加到output中
            for obj2 in author_data:
                last_played = readable_unixtime(obj2["last_played"])
                output_sus += f'{obj2["steamid"]},{obj2["num_games_owned"]},{obj2["num_reviews"]},{obj2["playtime_forever"]},{obj2["playtime_last_two_weeks"]},{obj2["playtime_at_review"]},%s' % str(
                    last_played)
            review_fix = str(obj["review"]).replace(',', '，')
            # f 为f-string格式化，将大括号中的表达式替代
            output_sus += f',{obj["recommendationid"]},{obj["language"]},{review_fix},%s,%s,{obj["voted_up"]},{obj["votes_up"]},{obj["votes_funny"]},{obj["weighted_vote_score"]},{obj["comment_count"]},{obj["steam_purchase"]},{obj["received_for_free"]},{obj["written_during_early_access"]},{obj["hidden_in_steam_china"]},{obj["steam_china_location"]},{review_len},{Is_updated}' % (
                str(timestamp_created), str(timestamp_updated))
    # 将结果写到到output.csv中
    # 游玩时间单位是分钟
    if sus_count == 0:
        print('恭喜!游戏大概是小众到没有可疑评论呢！')
    else:
        with open(jsfile_name + '-reviews_sus_post2.csv', 'w', encoding='gbk') as f:
            output_sus = output_sus.encode('gbk', "ignore")
            output_sus = output_sus.decode('gbk', "ignore")
            f.write(output_sus)
        print(
            str(sus_count) + "条可疑无效Reviews已隔离，请查看" + jsfile_name + '-reviews_sus_post2.csv CSV文件')
    with open(jsfile_name + '-reviews_post2.csv', 'w', encoding='gbk') as f:
        output2 = output2.encode('gbk', "ignore")
        output2 = output2.decode('gbk', "ignore")
        f.write(output2)
    print("Reviews后处理已完成，请查看" + jsfile_name + '-reviews_post2.csv CSV文件')
    return commentcloud


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # print_hi('PySteam')
    commentcloud = []
    # 词云遮罩，白色部分不绘制
    # img = mpimg.imread('steam~1.png')
    img = np.array(Image.open('steam3.png'))
    # print(img) #保证留白是255,255,255
    # img = plt.imread('steam3.png')
    # img = np.array(imageio.imread('steam.jpg'))
    is_ch = str(
        input("启用cookie?(输入0暂不启用，输入1启用, 输入2直接分析评论数据, 输入4传入人工清洗的【JS文件】进行词云处理):"))
    if is_ch == '4':
        jsfile_name = str(input("输入main程序同目录下【JS文件】名(不含后缀)，或使用绝对路径(注意双反写斜杠)):"))
        commentcloud = word_cloud_process(jsfile_name + '.json')
        word_cloud(img, commentcloud)
        exit()
    AppID = input("请输入Steam AppID:")
    if is_ch == '2':
        skip_cookie()
    else:
        game_name = get_basic_gameinfo(AppID)
    if is_ch == '1':
        get_game_achieve_cookie(AppID)
    else:
        get_game_achieve(AppID)  # 成就
    n = int(input("请输入获取数量:"))
    n2 = n
    flag = 0
    n2 = get_n_reviews(AppID, n2, n)
    flag = 1
    # flag_bytes = 1
    # readable_unixtime(1680409828)
    if not n2 == 0:
        Cursor = input("请回车以获取下一批评论（剩余%d条）,输入0以结束:" % n2)
        while Cursor is not None:
            try:
                n2 = get_n_reviews(AppID, n2, n, params['cursor'])
                Cursor = '*'
                if not n2 == 0:
                    Cursor = input("请回车以获取下一批评论（剩余%d条）,输入0以结束:" % n2)
                    if Cursor == "0" or Cursor == "*" or Cursor == '\n' or n2 == 0:
                        break
                else:
                    break
            except Exception as e:
                commentcloud = post_process()
                word_cloud(img, commentcloud)
                print(e)
                print("程序已结束")
                exit()
    else:
        commentcloud = post_process()
        word_cloud(img, commentcloud)
        exit()

    commentcloud = post_process()
    word_cloud(img, commentcloud)
    exit()
