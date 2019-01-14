__author__ = 'shine'

#!/usr/bin/env python
#-*-  coding：UTF-8  -*-

import urllib.request
import re
import csv
from datetime import datetime
import codecs


# def getlist() :
#
#     html = urllib.request.urlopen('http://bidding.sztu.edu.cn/xxgk/xqgs.htm').read()
#     html = html.decode('utf8')
#     # print(html)
#
#
#     reg = re.compile(r'<a href="(.*?)" target="_blank" title=".*?">(.*?)</a><span class="time">(.*?)</span>')
#     # mat = re.search(r'<span class="time">(.*?)</span>',html)
#     urls = re.findall(reg,html)
#     # print((urls))
#     # print(mat)
#     for url in urls:
#
#         s=url[0].replace("../../","/")
#         s1=s.replace("../","/")
#         link=("http://bidding.sztu.edu.cn"+s1)
#         subject=url[1]
#         time=url[2]
#         datas = [([subject,link,time])]
#         print(datas)

def getlist() :
    # linkurl=http://bidding.sztu.edu.cn/xxgk/xqgs.htm
    # for i in range(0,1):
    #     if i=0:
    #     linkurl=http://bidding.sztu.edu.cn/xxgk/xqgs.htm
    # else:
    #     linkurl=http://bidding.sztu.edu.cn/xxgk/xqgs+%i.htm

    html = urllib.request.urlopen('http://bidding.sztu.edu.cn/xxgk/xqgs.htm').read()
    html = html.decode('utf8')
    # print(html)


    reg = re.compile(r'<a href="(.*?)" target="_blank" title=".*?">(.*?)</a>')
    urls = re.findall(reg,html)
    # print((urls))
    for url in urls:

        s=url[0].replace("../../","/")
        s1=s.replace("../","/")
        link=("http://bidding.sztu.edu.cn"+s1)
        subject=url[1]
        datas = [([subject,link])]
        print(datas)

        with open(r'C:\Users\shine\Desktop\py爬虫\sztu.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in datas:
                writer.writerow(row)

getlist()






