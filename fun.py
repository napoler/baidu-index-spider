import re
import os
import time
import argparse
import requests
from multiprocessing import Pool


def seo(domain_url):
    """
    利用爱站接口查询权重信息
    """
    url = f'http://seo.chinaz.com/?host={domain_url}'
    headers = {
        'Host': 'seo.chinaz.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.get(url=url, headers=headers, timeout=6)
    html = r.text

    # 百度权重正则
    baidu_pattern = re.compile(r'baiduapp/(.*?).gif')
    baidu = baidu_pattern.findall(html)[0]

    # 站点标题正则
    site_name_rules = re.compile(r'class="ball">(.*?)</div>')
    site_name = site_name_rules.findall(html)[0]

    print(str(domain_url).ljust(30), '\t', baidu, '\t', site_name)
    return domain_url, int(baidu), site_name,time.time()


def domain_rank(lines):
    """
    lines为域名列表

    """
    #  设置一个容量为8的进程池
    # pool_number = 10
    # pool = Pool(pool_number)
    ranks=[]
    for line in lines:
        if 'http://' in line:
            line = line[7:]
        elif 'https://' in line:
            line = line[8:]
        if line:
            # pool.apply_async(seo, (line,))
            ranks.append(seo(line))
    return ranks
# ranks=domain_rank(["baidu.com"])
# print(ranks)