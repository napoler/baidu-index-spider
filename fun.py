import re
import os
import time
import argparse
import requests
from multiprocessing import Pool

from urllib.parse import urlparse
import tkitText
from config import *

def db_add_domain_rank(key,vaule):
    """
    保存对象
    vaule为对象
    """
    # print("data",vaule)
    data={"_id":key,'rank':vaule['rank'],'time':vaule['time']}
    # data={"_id":key,'rank':vaule['rank'],'site_name':value['site_name'],'time':vaule['time']}
    # print("data",data)
    try:
        DB.domain_rank.insert_one(data) 
        # print("err")
    except :
        # print("添加权重失败")
        DB.domain_rank.update_one({'_id':key},   {"$set" :data}) 



def db_add_domain_rank(key,vaule):
    """
    保存对象
    vaule为对象
    """
    # print("data",vaule)
    data={"_id":key,'rank':vaule['rank'],'time':vaule['time']}
    # data={"_id":key,'rank':vaule['rank'],'site_name':value['site_name'],'time':vaule['time']}
    # print("data",data)
    try:
        DB.domain_rank.insert_one(data) 
        # print("err")
    except :
        # print("添加权重失败")
        DB.domain_rank.update_one({'_id':key},   {"$set" :data}) 


def db_add_search_rank(key,data):
    """
    保存对象
    vaule为对象
    """
    try:
        DB.search_rank.insert_one(data) 
        # print("err")
    except :
        # print("添加权重失败")
        DB.search_rank.update_one({'_id':key},   {"$set" :data}) 

def db_get_search_rank(key):
    """
    搜索域名权重
    
    """
    try:
        return DB.search_rank.find_one({"_id":key}) 
    except :
        # del vaule['_id']
        # DB.domain_rank.update_one({'_id':key},   {"$set" :{"_id":key,'value':vaule}}) 
        return 

def db_add_keyword(keyword):
    """
    保存对象
    vaule为对象
    """
    data={"_id":keyword,"value":keyword}
    try:
        DB.keyword.insert_one(data) 
        # print("err")
    except :
        # print("添加权重失败")
        # DB.keyword.update_one({'_id':keyword},   {"$set" :data}) 
        pass

def db_get_keyword(keyword):
    """
    保存对象
    vaule为对象
    """
    data={"_id":keyword,"value":keyword}
    try:
        DB.keyword.find_one({"_id":keyword}) 
        return True
    except :
        return False
def set_cache(key,value,expire=60*60*24*1):
    try:
        DB.cache.insert_one({"_id":key,"value":value,'time':time.time()}) 
        return True
    except :
        return False    
def get_cache(key,expire=60*60*24*1):
    """
    获取缓存，超过时间自动清除
    
    """
    try:
        data=DB.cache.find_one({"_id":key})
        print(data)
        if data['time']-expire>0:
            print("有效")
            return data
            pass
        else:
            data=DB.cache.delete_one({"_id":key})
            print("过期已经自动清除！")
            return False 
        # return True
    except :
        return False 
        pass   

def seo(domain_url):
    """
    利用爱站接口查询权重信息
    """
    print("检查域名：",domain_url)
    try:
        domain_rank=db_get_domain_rank(domain_url)
        print("域名权重：",domain_rank)

        return domain_rank
        # if domain_rank:
        #     print("已经存在",domain_rank)
        #     return domain_rank
        # else:
        #     print("新域名权重")
        #     pass
    except:
        print("新域名权重")
        pass

    if get_cache("seo_"+domain_url):
        print("最近检查过域名跳过处理")
        return
    else:
        set_cache("seo_"+domain_url,'a')

    # print("2222")
    url = f'http://seo.chinaz.com/?host={domain_url}'
    headers = {
        'Host': 'seo.chinaz.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.get(url=url, headers=headers, timeout=6)
    print("status_code:",r.status_code)



    # get_cache("ee")
    # print("html", r.text)
    html = r.text

    # 百度权重正则
    baidu_pattern = re.compile(r'baiduapp/(.*?).gif')
    baidu = baidu_pattern.findall(html)[0]

    # 站点标题正则
    site_name_rules = re.compile(r'class="ball">(.*?)</div>')
    site_name = site_name_rules.findall(html)[0]

    # print(str(domain_url).ljust(30), '\t', baidu, '\t', site_name)
    value={
        "domain":domain_url,
        "rank":int(baidu),
        "site_name":site_name,
        "time":time.time()
    }
    # print("New",value)
    db_add_domain_rank(domain_url,value)
    # return domain_url, int(baidu), site_name,time.time()
    data={"_id":domain_url,'rank':vaule['rank'],'time':vaule['time']}
    # data={"_id":domain_url,"value":value}
    print("域名权重：",data)

    return data




def domain_rank(lines):
    """
    lines为域名列表

    """
    ranks=[]
    for line in lines:
        if 'http://' in line:
            line = line[7:]
        elif 'https://' in line:
            line = line[8:]
        if line:
            ranks.append(seo(line))
    return ranks


def url_domain(url):
    # url='http://www.leontom.cc/post/719.html'
    res=urlparse(url)
    # print("返回对象：", res)
    # print("域名", res.netloc)
    return {"domain":res.netloc,"path":res.path}


# url='http://www.leontom.cc/post/719.html'
# print(url_domain(url))


# url="www.leontom.cc"
# seo([url])