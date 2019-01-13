__author__ = 'shine'

#!/usr/bin/env python
#-*-  coding：UTF-8  -*-

import urllib.request
import re
import csv
import codecs

# def getlist() :
#     html = urllib.request.urlopen('http://bidding.sztu.edu.cn/xxgk/xqgs.htm').read()
#     html = html.decode('utf8')
#
#     reg = re.compile(r'<h2 class="cleafix"><a href="(.*?)" target="_blank" title=".*?">(.*?)</a><span class="time">(.*?)</span></h2>')
#     urls = re.findall(reg,html)
#     # print((urls))
#     for url in urls:
#         zx=("http://bidding.sztu.edu.cn"+url[0])
#         zt=url[1]
#         time=url[2]
#         datas = [([subject,link,time])]
#         print(datas)

def getlist() :
    html = urllib.request.urlopen('http://bidding.sztu.edu.cn/xxgk/xqgs.htm').read()
    html = html.decode('utf8')
    # print(html)


    reg = re.compile(r'<a href="(.*?)" target="_blank" title=".*?">(.*?)</a>')
    urls = re.findall(reg,html)
    # print((urls))
    for url in urls:
        # global zx,zt
        # global datas
        link=("http://bidding.sztu.edu.cn"+url[0])
        subject=url[1]
        datas = [([subject,link])]
        print(datas)

        with open(r'C:\Users\shine\Desktop\py爬虫\sztu.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in datas:
                writer.writerow(row)

getlist()






