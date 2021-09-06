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
	for item in center.find_all('center'):
		item.decompose()
	return center.text

def download(main_url):
	soup = BeautifulSoup(cached_url.get(main_url, encoding='gbk'), 'html.parser')
	novel_name = soup.find('h1').text
	result = []
	for sub_url in findLinks(soup):
		for count in range(1, 5):
			text = getText(main_url + sub_url.replace('.html', '_%d.html' % count))
			if not text.endswith('本章未完，点击下一页继续阅读'):
				result.append(text)
				break
			text = text.rsplit('本章未完，点击下一页继续阅读', 1)[0].strip()
			result.append(text)
	result = compactText('\n\n'.join(result))
	for item in ['&amp;', '—zwnj;', '&nbsp', '']:
		result = result.replace(item, '')
	with open('download/%s.txt' % novel_name, 'w') as f:
		f.write(result)
	
if __name__ == "__main__":
	download('https://www.mbtxt.la/go/94213/')