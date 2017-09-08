import requests
import threading
from lxml import etree


def get_html(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = requests.get(url=url,headers=header)
    response = req.text
    return response

def get_img_html(html):
    tree = etree.HTML(html)
    all_a = tree.xpath('//div[@class="col-sm-9"]/a/@href')
    for link in all_a:
        img_html = get_html(link)
        img_html += img_html
        return img_html

def get_img(html):
    tree = etree.HTML(html)
    items = tree.xpath('//div[@class="artile_des"]')
    for item in items:
        imgurl_list  = item.xpath('table/tbody/tr/td/a/img/@onerror')
        start_save_img(imgurl_list)


def save_img(img_url):
    img_url = img_url.split('=')[-1][1:-2].replace('.jp','.jpg').replace('.pn','.png').replace('.gi','.gif')
    print(u'正在下载'+'http:'+img_url)
    img_content = requests.get('http:'+img_url).content
    with open('D:\doutu\%s.jpg' % img_url.split('/')[-1],'wb') as f:
        f.write(img_content)


def start_save_img(imgurl_list):
    for i in imgurl_list:
        th = threading.Thread(target=save_img,args=(i,))
        th.start()

def main():
    start_url = 'https://www.doutula.com/article/list/?page={}'
    for i in range(1,500):
        print(i)
        start_html = get_html(start_url.format(i))
        html = get_img_html(start_html)
        get_img(html)

main()
print('爬取结束')
