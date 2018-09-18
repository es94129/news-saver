import os
import time
import codecs
from bs4 import BeautifulSoup
from selenium import webdriver

SCROLL_PAUSE_TIME = 1.5



def get_news_content(url):
	browser.get(url)

	date = url.split('/')[-2]
	if len(date) != 8:
		return

	index = 1
	if(date in dir_count):
		index = dir_count[date]
		dir_count[date] = index+1
	elif os.path.exists(date) == False:
		os.mkdir(date)
		dir_count[date] = 1
	else:
		dir_count[date] = 1


	filepath = date + "/" + str(index) + ".txt"
	f = codecs.open(filepath,"w","utf-8")

	#title and date
	f.write(browser.title + "	" + date + "\r\n")

	#paragraphs
	all_pars = browser.find_elements_by_class_name("one-p")
	for par in all_pars:
		f.write(par.text + "\r\n")
	f.close()

def target_link(link):
	if "20180912" in link:
		return True
	return False

def sector_news(url):
	news_count = 0

	# Get scroll height
	last_height = browser.execute_script("return document.body.scrollHeight")
	count = 0
	###
	while True:
		# Scroll down to bottom
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
		count += 1
		if count == 100:
			break

	links = []
	all_news = browser.find_elements_by_tag_name('h3')
	for news in all_news:
		if (len(news.text) == 0):
			continue
		link_elements = news.find_elements_by_tag_name('a')
		for link_element in link_elements:
			link = link_element.get_attribute('href')
			if link in filename_list:
				continue
			filename_list.append(link)
			if (".html" in link) and (target_link(link)):
				links.append(link)

	print(len(links))
	for link in links:
		get_news_content(link)


def traverse():
	entrance_url = "https://new.qq.com/"
	browser.get(entrance_url)
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	sector_links = ["/"]
	all_sect = soup.select("#main-list .item a")
	for sect in all_sect:
		sector_links.append(sect.get('href'))
	
	for link in sector_links:
		if ("omv" in link or "photo" in link):
			continue
		print(link)
		link = entrance_url[:-1] + link
		browser.get(link)
		sector_news(link)

#execution
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")
browser = webdriver.Chrome(chrome_options = chrome_options)
#browser = webdriver.Chrome()
#browser.maximize_window()

dir_count = {}
filename_list = []
traverse()

browser.close()
print("finished")
