#!/usr/bin/env python3
import requests
import argparse
from tqdm import tqdm
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException,InvalidArgumentException

def init(path):
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  #  interactive
    driver = webdriver.Chrome(executable_path=path,desired_capabilities=caps)
    driver.minimize_window()
    return driver

def readPage(driver,url):
    page = driver.get(url)
    allLinks = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for x in allLinks:
        try:
            l =  x.get_attribute('href')
            if l == '#' or l == '' :
                continue
            links.append(x.get_attribute('href'))
        except StaleElementReferenceException:
            continue
        except InvalidArgumentException:
            continue
    return links

def selectExtension(link,ext):
    if link.split('.')[-1] == ext:
        return True
    else:
        return False


def download(dir,url):
    fileName = url.split('/')[-1]
    dPath = os.path.join(dir,fileName)
    print("Downloading file : {f}".format(f=fileName))
    r = requests.get(url,stream=True)
    total_size = int(r.headers["Content-Length"])
    downloaded = 0  # keep track of size downloaded so far
    chunkSize = 1024
    bars = int(total_size / chunkSize)
    with open(dPath,'wb+') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunkSize),total=bars, unit='KB', desc=fileName, leave=True, file=sys.stdout):
            if chunk: 
                    f.write(chunk)
    print("Done downloading : {f}".format(f=fileName))


def main():
    ext = "pdf"
    downpath = "../../DSP_notes"
    try:
        os.mkdir(downpath)
    except:
        print("Directory exists")
    url = "https://ocw.mit.edu/resources/res-6-007-signals-and-systems-spring-2011/lecture-notes/"
    path = "./chromedriver"
    driver = None
    try:
        driver = init(path)
        links = readPage(driver,url)
        links = [x for x in links if selectExtension(x,ext) ]
        print("All links of extension .{ext} have been obtained".format(ext=ext))
        for x in links:
            download(downpath,x)
        print("Done")
    except Exception as e:
        print(e)
        print("Exiting")
    finally:
        driver.close()
main()
        