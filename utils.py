#!/usr/bin/env python3
import requests
import argparse
from tqdm import tqdm
import sys
import subprocess
from zipfile import ZipFile
from selenium import webdriver
import os

def getChromeDriver():
    try:
        driver = webdriver.Chrome(executable_path="./chromedriver")
        driver.close()
    except Exception as e:
        print(e)
        print("Downloading a new chromedriver as the current is unsuitable")
        fileName = ""
        platform = ""
        architecture = ""
        version = ""
        if sys.platform.startswith('win'):
            fileName = 'chromedriver.exe'
        else:
            fileName = 'chromedriver'
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'linux'
            architecture = '64'
        elif sys.platform == 'darwin':
            platform = 'mac'
            architecture = '64'
        elif sys.platform.startswith('win'):
            platform = 'win'
            architecture = '32'
        else:
            raise RuntimeError('Could not determine chromedriver download URL for this platform.')
        #print(platform,architecture)
        if platform == 'linux':
            with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').replace('Chromium', '').strip()
                version = version.replace('Google Chrome', '').strip()
        elif platform == 'mac':
            process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
            version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
        elif platform == 'win':
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
            )
            version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
        else:
            return
        print(version)
        maj = version.split(".")[0]
        print("Please wait while getting data.....")
        ver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{m}".format(m = maj)
        data = requests.get(ver_url)
        current = data.content.decode('utf-8')
        zipName = "chromedriver_{p}{a}.zip".format(p = platform,a = architecture)
        down_url = "https://chromedriver.storage.googleapis.com/{c}/{z}".format(c = current,z = zipName)
        print(current,down_url)
        r = requests.get(down_url,stream=True)
        total_size = int(r.headers["Content-Length"])
        chunkSize = 1024
        bars = int(total_size / chunkSize)
        with open(zipName,'wb+') as f:
            for chunk in tqdm(r.iter_content(chunk_size=chunkSize),total=bars, unit='KB', desc=fileName, leave=True, file=sys.stdout):
                if chunk: 
                        f.write(chunk)
        print("Chromedriver has completed downloading....")
        with ZipFile(zipName,"r") as zip:
            zip.extract('chromedriver',"./")
        os.remove(zipName)
        os.chmod("./chromedriver",755)
    finally:
        print("Chromedriver is working now")

getChromeDriver()