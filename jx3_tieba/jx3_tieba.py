# -*- coding: utf-8 -*-
"""
@author: MonsterHe
@contact: yuntian.hee@gmail.com
@version: python3.6
@file: jx3_tieba.py
@time: 2018/10/5 11:34
"""
import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except:
        return " Error "

def get_content(url):
    '''
    获取贴吧的标题、作者等信息
    :param url:
    :return:
    '''
    comments = []

    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    # 找到所有包含需要信息的li标签
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    for li in liTags:
        # 初始化一个字典存储文章信息
        comment = {}
        # 这里使用一个try except防止爬虫找不到信息从而停止运行
        try:
            # 开始筛选信息
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = 'https://tieba.baidu.com' + \
                               li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['author'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print(' 解析规则出了问题 ')
    return comments


def Out2File(dict):
    '''
    将爬取到的文件写入到本地
    并保存到当前目录的 JX3tieba.txt中
    '''
    with open('JX3tieba.txt', 'a+') as f:
        for comment in dict:
            f.write('标题：{} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量：{} \n'
                    .format(comment['title'], comment['link'], comment['author'], comment['time'], comment['replyNum']))

        print('当前页面爬取完成')

def main(base_url, deep):
    url_list = []
    # 将所有需要爬取的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))

    print('当前爬取页数：{}'.format(deep) + ' 开始筛选信息...')

    # 循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)

base_url = "https://tieba.baidu.com/f?kw=%e5%89%91%e7%bd%913剑网3&ie=utf-8"
deep = 3

if __name__ == '__main__':
    main(base_url, deep)

