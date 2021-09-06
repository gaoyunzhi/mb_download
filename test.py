#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cached_url
from bs4 import BeautifulSoup
from telegram_util import compactText
import os

def findLinks(soup):
	for x in soup.find_all('a', class_='sosad-button'):
		yield x['href']

def getSoup(url, force_cache = True, cookie = None):
	return BeautifulSoup(cached_url.get(url, {'cookie': cookie}, 
		force_cache = force_cache), 'html.parser')

def getMainContent(link, cookie = None):
	sub_soup = getSoup(link, force_cache = True, cookie = cookie)
	return sub_soup.find('div', class_='main-text')

def getText(link):
	main_content = getMainContent(link, cookie = None)
	if not main_content:
		os.system('rm %s' % cached_url.getFilePath(link))
		main_content = getMainContent(link, cookie = cookie)
	for att in ['font-4', 'text-left']:
		item = main_content.find('div', class_=att)
		if item:
			item.decompose()
	return main_content.get_text(separator='\n')

def download(url):
	soup = BeautifulSoup(cached_url.get(url), 'html.parser')
	novel_name = soup.find('h1').text
	print(novel_name.encode('utf-8').decode('gbk'))
	# result = []
	# for link in findLinks(soup):
	# 	result.append(getText(link))
	# with open('download/%s.txt' % novel_name, 'w') as f:
	# 	f.write(compactText(''.join(result)))
	
if __name__ == "__main__":
	download('https://www.mbtxt.la/go/94213/')