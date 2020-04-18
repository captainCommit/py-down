#!/usr/bin/env python3
import requests
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

def init(p):
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  #  interactive
    driver = webdriver.Chrome(executable_path=p,desired_capabilities=caps)
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
    if os.path.exists(dir):
        pass
    else:
        print('x')
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
    print("Done downloading : {f}".format(f=fileName))


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
    os.system('clear')
    print("################### Downloader v1.0 ###################")
    d = None
    p= None
    l = None
    if os.path.exists('config.env'):
        f = load_dotenv('config.env')
        d = os.getenv("d")
        p = os.getenv("p")
        l = os.getenv("l")
    else:
        print("This data is only needed for the first run for configuration.\n")
        d = input("location of the chromedriver file : ")
        p = input("location of the text file containing list of urls : ")
        l = input("destination of downloaded files : ")
        f = open('config.env','w+')
        f.write("d={d}\np={p}\nl={l}".format(d=d,p=p,l=l))
        f.close()

    #print("Enter download data")
    #print("-------------------------")
    t = "video"#input('tag containing the url : ')
    a = "src"#input('the attribute that holds the url to the file : ')
    e = "mp4"#input("extension of the file being downloaded : ")

    driver = init(str(d))
    urls = getlinks(p)
    for url in urls:
        links = getUrls(driver,urls,t,a)
        for x in links:
            download(l,x,e)
        print("Done")
except Exception as qw:
    driver.close()
    print(qw)
    print("Encountered Error Exiting...... ")
    exit(0)