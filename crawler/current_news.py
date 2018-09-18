import codecs
from bs4 import BeautifulSoup
import requests
def get_current_news():
	html = get_html_text("http://news.qq.com/")
	soup = BeautifulSoup(html, 'html.parser')

	tags = soup.find_all("a","linkto")
	news = {}
	f = codecs.open("current_news.txt","w","utf-8")
	for tag in tags:
		title = tag.get_text()
		link = tag.get("href")
		news[title] = link
		f.write(title + "\r\n")
		f.write(link + "\r\n")
	f.close()