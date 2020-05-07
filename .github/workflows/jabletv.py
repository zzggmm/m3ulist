# coding:UTF-8
import ssl
import requests
from lxml import etree
import json

ssl._create_default_https_context = ssl._create_unverified_context
# 屏蔽warning信息
requests.packages.urllib3.disable_warnings()

def my_requests(url):
    try:
        response = requests.get(url,verify=False)
    except:
        print("网络请求异常，正在重试！")
        response = requests.get(url,verify=False)
    response.encoding = 'UTF-8'
    selector = etree.HTML(response.text)
    return selector

def write_to_file(content):
    with open(path,'a+',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False))

def get_m3u(url):
    print('开始处理网页：',url)
    html_sel = my_requests(url)
    title = html_sel.xpath('//*[@id="site-content"]/div/div/div[1]/section[2]/div[1]/div[1]/h4/text()')[0]
    logo = html_sel.xpath('/html/head/meta[7]/@content')[0]
    m3u_url = html_sel.xpath('//*[@id="site-content"]/div/div/div[1]/section[1]/link/@href')
    if len(m3u_url) != 0:
        m3u_url = html_sel.xpath('//*[@id="site-content"]/div/div/div[1]/section[1]/link/@href')[0]
        dic = {"name": title,
               "referer":url,
               "logo": logo,
               "url": m3u_url,
               }
        write_to_file(dic)
        with open(path, 'a+') as f:
            f.write(',' + '\n')
    else:
        print(url + '该页面为收费页面或者错误')

def get_html(url):
    html_sel = my_requests(url)
    html_url = html_sel.xpath('//*[@id="list_videos_common_videos_list"]/div/section/div/div/div/div[1]/a/@href')
    return html_url

path = '1.txt'



for i in range(1,202):
    html_list= get_html('https://jable.tv/hot/' + str(i) +'/')
    print(i)
    for url in html_list:
        get_m3u(url)
