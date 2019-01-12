#coding=utf-8
import re
import time
import random
import urllib.request
import urllib.parse
import pymysql
import chardet

from bs4 import BeautifulSoup

# 通过一个url获取html内容，这部分基本没有动
def url_open(url, page_num):

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')

    proxies=['39.137.69.8:8080','39.137.69.9:80','39.137.69.6:80','39.137.69.10:80','221.130.253.135:8090']
    proxy= random.choice(proxies)

    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    #urllib.request.install_opener(opener)

    #这里的postdata就是模拟点击某一页
    post_data = urllib.parse.urlencode({'pageNum':page_num}).encode('utf-8')
    response = urllib.request.urlopen(url=req,data=post_data)
    html= response.read()

    # 直接返回html并解析存在bug，目前还没找到原因，所以使用文件保存html 然后使用bs解析文件
    file = open('cache.html','w')
    file.write(html.decode('utf-8'))
    file.close()

    return html

# 新建一个csv文件，并添加好标题
def make_record_file():
    # w方法的打开方式是清空之前的内容
    csv = open(saved_filename,'w')
    csv.write('发布单位,主题,设备类别,发布时间,截标时间,链接\n')
    csv.close()

# 向csv文件中追加一条记录
def record_info(agency, subject, device,releaseDate,deadline,link):
    # a方法的打开方式是追加的方式
    csv = open(saved_filename,'a')
    csv.write('%s,%s,%s,%s,%s,%s\n'%(agency, subject, device,releaseDate,deadline,link))
    csv.close()

# 根据html获取对应的记录并保存
def fetch_info(html):
    # 读取刚刚保存的文件
    soup = BeautifulSoup(open('cache.html'),'html5lib')

    # 根据网页内容，获取特定的table标签
    table = soup.find(name='table',attrs={'id':'contentTable'})
    # 遍历table标签下所有的tr标签,[1:]表示从第二行开始，也就是忽略了标题
    for tr in table.find_all(name='tr')[1:]:
        # 根据它的特点找到链接、各项内容等等
        link = urllib.parse.urljoin(
            url_prefix, tr.get('onclick').split('\'')[1])
        strs = []

        for td in tr.find_all('td'):
            # 有的是font标签有的是span标签
            tag = td.find('font') or td.find('span')
            if tag == None:
                strs.append(' ')
            else:
                # 有的内容为空，因此在这儿处理一下
                string = tag.string or ' '
                #去掉换行、逗号，以防止混淆csv文件
                string = string.replace('\n','').replace('\r','').replace(',',' ')
                strs.append(string)

        agency, subject, device,releaseDate,deadline = strs

        # 保存
        record_info(agency, subject, device,releaseDate,deadline,link)

# 依次处理每一页
def process():

    # 循环处理每一页，i对应的是第i+1页
    for i in range(0, nb_pages):

        # 输出当前在处理第几页
        print('正在抓取第%d页内容...'%(i+1))

        # 获取这一页的内容并保存
        fetch_info(url_open(url_prefix, page_num = i + 1))

        # 防止过快的抓取网站会被封ip
        time.sleep(random.randint(0,waiting_seconds))

if __name__== '__main__':

    """ 配置信息 """

    # 总页数
    nb_pages = 44

    # 保存的文件名
    saved_filename = 'highschool.csv'

    # 两次抓取的间隔时间（秒）, 我看到上面你用了代理，所以这儿可以设的短一些，2秒即可,这样25页50秒就可以完成
    waiting_seconds = 0

    # 网页前缀
    url_prefix = "http://www.soeasycenter.com/morebiddingneed/need"

    # 新建一个csv文件，用来保存所有的记录
    make_record_file()

    # 开始处理
    process()
