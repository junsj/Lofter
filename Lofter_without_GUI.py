from bs4 import BeautifulSoup
import urllib
import urllib.request
import re
import os


def get_single_page(url,decode='utf-8'):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    response = urllib.request.Request(url=url, headers=headers)  
    html = urllib.request.urlopen(response,timeout=20).read().decode(decode,errors='ignore')
    return html

def get_pages(url,start_page=1,end_page=None):
    all_pages = []
   
    if end_page == None:
        pages = None
        while pages != []:
            pages = []
            page_url = url + str(start_page)
            html = get_single_page(page_url)
            soup = BeautifulSoup(html,"html.parser")
            pages = re.compile(r'"(http://.*.lofter.com/post/.*?)"').findall(str(soup))
            all_pages = all_pages + pages 
            start_page += 1
    else:
        for page in range(start_page,end_page+1):
            pages = []
            page_url = url + str(page)
            print(page_url)
            html = get_single_page(page_url)
            soup = BeautifulSoup(html,"html.parser")
            pages = re.compile(r'"(http://.*.lofter.com/post/.*?)"').findall(str(soup))
            all_pages = all_pages + pages
    all_pages = list(set(all_pages))
    return all_pages

def download_single_page(url,download_to):

    img_class = "(img)|(image)|(pic)|(postphoto)"
    
    if not os.path.exists(download_to):
            os.makedirs(download_to)
        
    html = get_single_page(url,decode='utf-8')
    soup = BeautifulSoup(html,"html.parser")
    soup_div = soup.findAll("div",{"class":re.compile(img_class)})
    images = re.compile(r'bigimgsrc="(http://.*?.jpg).*?').findall(str(soup_div))
    for image in images:
        try:
            img1,img2 = os.path.split(image)
            filename = download_to + '\\' + img2
            if not os.path.exists(filename):
                urllib.request.urlretrieve(image,filename)
                print('Download Image:',image)
        except:
            print('@-@,Download Image Fail:',image)
    return images


'''
===============================================================================
Main Program: lofter webcrawler V18.0
Date: 2018/02/20
Author: YuN   
===============================================================================
'''

user_id = input('Lofter User:')

if user_id is '':
    user_id = 'huayoulaoshi'

url = 'http://' + user_id + '.lofter.com/?page='

download_to = 'files' + '\\' + user_id


print('正在评估总页数...')
all_pages = get_pages(url)

pn = len(all_pages)
print('评估完成,共',pn,'页')
i = 1

for page in all_pages:
    print('开始下载第',str(i),'/',pn,'页:',page)
    print('='*100)
    try:
        download_single_page(page,download_to)
    except:
        print('下载第',str(i),'页失败!')
    print('='*100)
    print('')
    i += 1
    


