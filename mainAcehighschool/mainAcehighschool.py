__author__ = 'shine'

#!/usr/bin/env python
#-*-  coding：UTF-8  -*-

import re
import time
import random
import urllib
import urllib.parse
import urllib.request
import bs4
from bs4 import BeautifulSoup

# 建立这个是因为简单的爬虫无法直接爬到采购类型（这是页面加载完成后JS的生成的）
# 因此需要建立这个字典，将代码转换为具体的类型
type_dict = {
     '974':  '公开招标',  '975':  '询价公告',
     '978':'竞争性谈判',  '977':  '单一来源',
     '979':  '资格预审',  '976':  '邀请公告',
     '982':  '中标公告',  '981':  '更正公告',
     '990':  '其他公告',  '984':  '其他公告',
     '998':  '公开招标',  '997':  '询价公告',
     '996':  '邀请公告',  '999':  '单一来源',
     '985':  '其他公告', '2653':'竞争性磋商',
    '2655':  '成交公告', '2656':  '终止公告',
    '1001':  '资格预审', '1000':'竞争性谈判',
    '1004':  '中标公告', '1003':  '更正公告',
    '1012':  '其他公告', '1006':  '其他公告',
    '1007':  '其他公告', '2654':'竞争性磋商',
    '2657':  '成交公告', '2658':  '终止公告'
}

# 通过一个url获取html内容，这部分基本没有动
def url_open(url):

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
    proxies=['39.137.69.8:8080','39.137.69.9:80','39.137.69.6:80','39.137.69.10:80','221.130.253.135:8090']
    proxy= random.choice(proxies)
    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(url)
    html= response.read()


    file = open('cache1.html','w')
    file.write(html.decode('utf-8'))
    file.close()

    return html


# 新建一个csv文件，并添加好标题
def make_record_file():
    # w方法的打开方式是清空之前的内容
    csv = open(saved_filename,'w')
    csv.write('采购类型,发布时间,地域,采购单位\n')
    csv.close()

# 向csv文件中追加一条记录
def record_info( btype, date, province, agency):
    # a方法的打开方式是追加的方式
    csv = open(saved_filename,'a')
    csv.write('%s,%s,%s,%s,\n'%( btype, date, province, agency))
    csv.close()

# 根据html获取对应的记录并保存
def fetch_info(html):

    soup = BeautifulSoup(html,"html.parser")

    # soup = BeautifulSoup(open('cache1.html'),'html5lib')
    # 根据网页内容，获取特定的ul标签


    ul_tag = soup.find(name='ul',attrs={'class':"c_list_bid"})
    # reg = re.compile(r'<a href="(.*?)" target="_blank" title=".*?">(.*?)</a>')
    # urls = re.findall(reg,html)
    # for url in urls:
    #     zx=url[0]
    #     print(zx)
    li = soup.find(name='li',attrs={'class':"c_list_bid"})
    # 遍历ul标签下所有的li标签
    for li_tag in ul_tag.find_all(li,ul):

        # title = li_tag.title.split()
        # return title.encode('utf8')

        # 准备获取其它内容
        em = li_tag.find_all('em')

        # 从第一个em标签中获取类型，此处需要根据type_dict将代码转换为对应的文字类型
        btype = type_dict[em[0].string]

        # 从第二个em标签中获取日期时间
        date = em[1].string

        # 从第三个em标签中获取地点（省份）
        province = em[2].string

        # 从第四个em标签中获取采购人（机构）
        agency = em[3].string

        # href = url_prefix+li_tag.href.split()
        # return href.encode('utf8')
        # 将这些信息保存在文件中
        record_info( btype, date, province, agency)


# 依次处理每一页
def process():
    # 第一页不用加号码，直接加'.htm'即可
    print('正在抓取第1页内容...')
    fetch_info(url_open(url_prefix+'.htm'))

    # 后几页循环处理，从i=1开始，i对应的是第i+1页
    for i in range(1, nb_pages):

        # 输出当前在处理第几页
        print('正在抓取第%d页内容...'%(i+1))

        # 组合当前的网址
        url = url_prefix+'_{}.htm'.format(i)
        # print (url)
        # 获取这一页的内容并保存
        # fetch_info(url_open(url_prefix, page_num = i + 1))
        fetch_info(url_open(url))

        # 防止过快的抓取网站会被封ip
        time.sleep(waiting_seconds)

if __name__== '__main__':

    """ 配置信息 """

    # 总页数
    nb_pages = 25

    # 保存的文件名
    saved_filename = 'result.csv'

    # 两次抓取的间隔时间（秒）, 我看到上面你用了代理，所以这儿可以设的短一些，2秒即可,这样25页50秒就可以完成
    waiting_seconds = 5

    # 网页前缀
    url_prefix = "http://www.ccgp.gov.cn/cggg/dfgg/index"

    # 新建一个csv文件，用来保存所有的记录
    make_record_file()

    # 开始处理
    process()