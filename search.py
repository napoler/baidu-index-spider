# https://github.com/napoler/MagicBaidu?organization=napoler&organization=napoler

import sys
#print(sys.path)
#加载丢失的python libary path
# sys.path.append("/usr/local/lib/python3.7/site-packages")
#print(sys.path)
 
import requests
import re
import traceback
from urllib.request import quote
import getopt
from bs4 import BeautifulSoup

from fun import *
from config import *
import tkitText



class crawler:
    '''爬百度搜索结果的爬虫'''
    url = ''
    urls = []
    o_urls = []
    html = ''
    total_pages = 5
    current_page = 0
    next_page_url = ''
    timeout = 60                    #默认超时时间为60秒
    headersParameters = {    #发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
 
    def __init__(self, keyword):
        self.keyword=keyword
        self.url = 'https://www.baidu.com/baidu?wd='+quote(keyword)+'&tn=monline_dg&ie=utf-8'
 
    def set_timeout(self, time):
        '''设置超时时间，单位：秒'''
        try:
            self.timeout = int(time)
        except:
            pass
 
    def set_total_pages(self, num):
        '''设置总共要爬取的页数'''
        try:
            self.total_pages = int(num)
        except:
            pass
 
    def set_current_url(self, url):
        '''设置当前url'''
        self.url = url
 
    def switch_url(self):
        '''切换当前url为下一页的url
           若下一页为空，则退出程序'''
        if self.next_page_url == '':
            sys.exit()
        else:
            self.set_current_url(self.next_page_url)
 
    def is_finish(self):
        '''判断是否爬取完毕'''
        if self.current_page >= self.total_pages:
            return True
        else:
            return False
 
    def get_html(self):
        '''爬取当前url所指页面的内容，保存到html中'''
        r = requests.get(self.url ,timeout=self.timeout, headers=self.headersParameters)
        if r.status_code==200:
            self.html = r.text
            print("-----------------------------------------------------------------------")
            print("[当前页面链接]: ",self.url)
            #print("[当前页面内容]: ",self.html)
            print("-----------------------------------------------------------------------")
            self.current_page += 1
        else:
            self.html = ''
            print('[ERROR]',self.url,'get此url返回的http状态码不是200')
    def get_titles(self):
        soup = BeautifulSoup(self.html, "html.parser")
        start=0
        now = start + 1
        o_urls=[]
        titles=[]
        for item in soup.find_all('h3','t'):
            # print(item.get_text())
            # print(item.a['href'])
            if item.a['href'].startswith("/"):
                pass
            else:
                o_urls.append(item.a['href'])
                titles.append(item.get_text())
        self.o_urls = o_urls
        self.o_titles = titles
        #取下一页地址
        next = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', self.html)
        if len(next) > 0:
            self.next_page_url = 'https://www.baidu.com'+next[-1]
        else:
            self.next_page_url = ''

    def get_keywords(self):
        soup = BeautifulSoup(self.html, "html.parser")
        getkws = soup.select("#rs a")
        for it in getkws:
            # print(it['href'])
            print(it.get_text())
            if len(it.get_text())>0:
                db_add_keyword(it.get_text())

    def get_urls(self):
        '''从当前html中解析出搜索结果的url，保存到o_urls'''
        o_urls = re.findall('href\=\"(http\:\/\/www\.baidu\.com\/link\?url\=.*?)\" class\=\"c\-showurl\"', self.html)
        o_urls = list(set(o_urls))  #去重

        self.o_urls = o_urls
        #取下一页地址
        next = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', self.html)
        if len(next) > 0:
            self.next_page_url = 'https://www.baidu.com'+next[-1]
        else:
            self.next_page_url = ''
    #  def get_titles(self):
    #     '''从当前html中解析出搜索结果的url，保存到o_urls'''
    #     o_urls = list(set(o_urls))  #去重
    #     titles = re.findall('href\=\"(http\:\/\/www\.baidu\.com\/link\?url\=.*?)\" class\=\"c\-showurl\"', self.html)
    #     self.o_urls = o_urls
    #     #取下一页地址
    #     next = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', self.html)
    #     if len(next) > 0:
    #         self.next_page_url = 'https://www.baidu.com'+next[-1]
    #     else:
    #         self.next_page_url = ''
 
    def get_real(self, o_url):
        '''获取重定向url指向的网址'''
        r = requests.get(o_url, allow_redirects = False)    #禁止自动跳转
        if r.status_code == 302:
            try:
                return r.headers['location']    #返回指向的地址
            except:
                return "http://www.baidu.com"+r.headers['location']    #返回指向的地址
                pass
        else:
            print("errr")
        return o_url    #返回源地址
 
    def transformation(self):
        '''读取当前o_urls中的链接重定向的网址，并保存到urls中'''
        self.urls = []
        self.titles=[]
        for i,(o_url,title) in enumerate(zip(self.o_urls,self.o_titles)):
            # print("o_url",o_url)
            try:
                self.urls.append(self.get_real(o_url))
                self.titles.append(title)
            except:
                pass
 
    def print_urls(self):
        '''输出当前urls中的url'''
        tt=tkitText.Text()
        for i,url in enumerate(self.urls):
            # print("url:",url)
            if url.startswith("/"):
                continue
            d=url_domain(url)
            # print("d",d)
            try:
                ranks=domain_rank([d['domain']])
                # print("ranks:",ranks)
            except:
                # print("domain err")
                pass
            # print("url:",url)
            d['url']=url
            d['title']=str(self.titles[i])
            d['page']=self.page
            d['i']=i
            d['keyword']=self.keyword
            
            md5=tt.md5(url)
            d['_id']=md5
            d['time']=self.time
            print("d",d)
            db_add_search_rank(md5,d)


 
    def print_o_urls(self):
        '''输出当前o_urls中的url'''
        for url in self.o_urls:
            print(url)
 
    def run(self):
        self.page=0
        self.time=time.time()
        while(not self.is_finish()):
            c.get_html()
            # c.get_urls()
            c.get_titles()
            # print("page",self.page)
            c.transformation()
            c.print_urls()
            c.switch_url()
            self.page+=1
        c.get_keywords()
 
# if __name__ == '__main__':
#     help = 'baiduSpider.py -k <keyword> [-t <timeout> -p <total pages>]'
#     keyword = None
#     timeout  = None
#     totalpages = None
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "hk:t:p:", [
#                                    "keyword=", "timeout=", "totalpages="])
#     except getopt.GetoptError:
#         print(help)
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print(help)
#             sys.exit()
#         elif opt in ("-k", "--keyword"):
#             keyword = arg
#         elif opt in ("-t", "--timeout"):
#             timeout = arg
#         elif opt in ("-p", "--totalpages"):
#             totalpages = arg
#     if keyword == None:
#         print(help)
#         sys.exit()
 
#     c = crawler(keyword)
#     db_add_keyword(keyword)
#     if timeout != None:
#         c.set_timeout(timeout)
#     if totalpages != None:
#         c.set_total_pages(totalpages)
# c.run()

if __name__ == '__main__':
    num=10000
    for it in DB.keyword.aggregate( [ { "$sample": { 'size': num } } ] ):
        keyword=it['_id']
        print("抓取关键词：",keyword)
        c = crawler(keyword)
        # if timeout != None:
        #     c.set_timeout(timeout)
        # if totalpages != None:
        #     c.set_total_pages(totalpages)
        c.run()