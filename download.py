#!/usr/bin/env python3
import requests
from utils import getChromeDriver
import os
import argparse
from tqdm import tqdm
import sys
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException,InvalidArgumentException

def init():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  #  interactive
    driver = webdriver.Chrome(executable_path="./chromedriver",desired_capabilities=caps)
    driver.minimize_window()
    return driver


def getlinks(path):
    f = open(path).readlines()
    links = [x.replace('\n','') for x in f]
    if len(links) == 0:
        print("No Link Provided in links in text file\nExiting....")
        raise Exception;
    return links

def getUrls(driver,urls,tag,attr):
    driver.get(url)
    l = driver.find_elements_by_tag_name(tag)
    v = [link.get_attribute(attr) for link in l]
    return v

def selectExtension(link,ext):
    if link.split('.')[-1] == ext:
        return True
    else:
        return False

def download(dir,url,ext):
    fileName = url.split('/')[-1].split('?')[0]
    if not fileName.startsWith("xvideos"):
        return
    if os.path.exists(dir):
        pass
    else:
        print('folder does not exist.... creating folder')
        os.mkdir(dir)
    dPath = os.path.join(dir,fileName)
    r = requests.get(url,stream=True)
    total_size = int(r.headers["Content-Length"])
    chunkSize = 1024
    bars = int(total_size / chunkSize)
    with open(dPath,'wb+') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunkSize),total=bars, unit='KB', desc=fileName, leave=True, file=sys.stdout):
            if chunk: 
                    f.write(chunk)
    print("{f} : download completed".format(f=fileName))


'''
parser = argparse.ArgumentParser(description="Download mutiple files from internet at once")
parser.add_argument('--d',type=str,help='location of the chromedriver file')
parser.add_argument('--p', type=str,help='location of the text file containing list of urls')
parser.add_argument('--t',type=str,help='tag containing the url')
parser.add_argument('--a',type=str,help='the attribute that holds the url to the file')
parser.add_argument('--e',type=str,help="extension of the file being downloaded")
parser.add_argument('--l',type=str,help="destination directory for storing downloaded files")
args = parser.parse_args()
'''
try:
    getChromeDriver()
    os.system('clear')
    print("################### Downloader v1.0 ###################")
    p= None
    l = None
    if os.path.exists('config.env'):
        ch = input("Do you want to change existing config files (Y/n): ")
        if ch.lower() == 'y':
            p = input("Link Repository : ")
            l = input("Destination Folder : ")
            t = input('Container Tag : ')
            a = input('Attribute : ')
            e = input("Extension : ")
            f = open('config.env','w+')
            f.write("links={p}\ndest={l}\ntag={t}\nattr={a}\next={e}".format(p=p,l=l,t=t,a=a,e=e))
            f.close() 
        else:
            f = load_dotenv('config.env')
            p = os.getenv("links")
            l = os.getenv("dest")
            t = os.getenv('tag')
            a = os.getenv('attr')
            e = os.getenv('ext')
    else:
        print("This data is compulsory in the first run to create a config file.\n")
        p = input("Link Repository : ")
        l = input("Destination Folder : ")
        t = input('Container Tag : ')
        a = input('Attribute : ')
        e = input("Extension : ")
        f = open('config.env','w+')
        f.write("links={p}\ndest={l}\ntag={t}\nattr={a}\next={e}".format(p=p,l=l,t=t,a=a,e=e))
        f.close() 

    driver = init()
    urls = getlinks(p)
    for url in urls:
        links = getUrls(driver,urls,t,a)
        for x in links:
            download(l,x,e)
except Exception as qw:
    driver.close()
    print(qw)
    print("Encountered Error Exiting...... ")
    exit(0)