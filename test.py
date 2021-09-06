#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cached_url
from bs4 import BeautifulSoup
from telegram_util import compactText
import os

def findLinks(soup):
	center = soup.find('div', id='list-chapterAll')
	for item in center.find_all('a', href=True):
		yield item['href']

def getText(link):
	soup = BeautifulSoup(cached_url.get(link, encoding='gbk'), 'html.parser')
	center = soup.find('div', class_='readcontent')
	return center.text

def download(main_url):
	soup = BeautifulSoup(cached_url.get(main_url, encoding='gbk'), 'html.parser')
	novel_name = soup.find('h1').text
	result = []
	for sub_url in findLinks(soup):
		result.append(getText(main_url + sub_url))
	with open('download/%s.txt' % novel_name, 'w') as f:
		f.write(compactText(''.join(result)))
	
if __name__ == "__main__":
	download('https://www.mbtxt.la/go/94213/')