from bs4 import BeautifulSoup

import urllib
import urllib.request
import re
import os

from PySide import QtCore, QtGui
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide import QtGui
from PySide.QtCore import *

import sys
import threading

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

            print(page_url)
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

def start_process_url(url,rooturl,download_to):
    print(url)
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



class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(400,60)
        self.setWindowTitle("Lofter User")
        
        hbox1 = QHBoxLayout()
        self.label_id1 = QLabel('Lofter User:')
        self.path_id1 = QLineEdit('',self)
        self.button_start = QPushButton('开始抓取',self)
        self.button_start.clicked.connect(self.process_start)

        hbox1.addWidget(self.label_id1)
        hbox1.addWidget(self.path_id1)
        hbox1.addWidget(self.button_start)
#        self.button_path.clicked.connect(self.setOpenFileName)

        hbox2 = QHBoxLayout()    
        self.label_id2 = QLabel('Download To:')
        self.path_id2 = QLineEdit('',self)

        hbox2.addWidget(self.label_id2)
        hbox2.addWidget(self.path_id2)
                
        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1,0)
        vbox.addLayout(hbox2,0)
        self.setLayout(vbox)    

    def process_start(self):
        user = self.path_id1.text()
        if user is '':
        #    user = 'zhaofangfang'
             user = 'kiiiingz'
        if self.path_id2.text() == '':
            download_to = user
        else:
            download_to = self.path_id2.text() + '\\' + user

        if not os.path.exists(download_to):
                    os.makedirs(download_to)
        url = 'http://' + user + '.lofter.com/?page='
        rooturl = url
 
        t = threading.Thread(target=start_process_url,args=(url,rooturl,download_to,))
        t.setDaemon(True)
        t.start()


myApp = QApplication(sys.argv)
myWindow = MainWindow()
myWindow.show()
myApp.exec_()
sys.exit(0)  
