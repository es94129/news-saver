import os
import codecs
import jieba

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsite.settings')

import django
django.setup()

from blog.models import News, Word

def save_word_model():
	newss = News.objects.all()
	for news in newss:
		seg_list1 = jieba.lcut(news.title)
		#print(len(seg_list1))
		seg_list2 = jieba.lcut(news.content)
		#print(len(seg_list2))
		word_list = []
		for seg in seg_list1:
			if (len(seg) > 1) and (seg != '\r\n') and (seg not in word_list):
				word_list.append(seg)
		for seg in seg_list2:
			if (len(seg) > 1) and (seg != '\r\n') and (seg not in word_list):
				word_list.append(seg)
		#print(len(word_list))
		
		for word in word_list:
			try:
				cur_word = Word.objects.get(spell=word)
				news.words.add(cur_word)
			except:
				cur_word = Word(spell=word)
				cur_word.save()
				news.words.add(cur_word)
		

"""
def save_word_model():
	count = 0
	print("hello hello")
	search_dir = os.getcwd()[:-7] + "search"
	word_list = os.listdir(search_dir)

	for word_file in word_list:
		count += 1
		if count <= 29504:
			continue

		word_spell = word_file[:-4]
		word = Word(spell=word_spell)
		word.save()

		f = codecs.open(search_dir+"/"+word_file,"r","utf8")
		s = f.read()
		f.close()

		indices = s.split(',')
		index_count = 0
		newss = []
		for index in indices:
			index_count += 1
			if index_count == 999:
				break
			if News.objects.filter(filepath=index).count() != 0:
				news = News.objects.get(filepath=index)
				#news.save()
				newss.append(news)
				#word.newss.add(news)
				#word.save()

		word.newss.add(*newss)
		print(count)
"""
def get_files(dir):
	file_list = os.listdir(dir)
	for file in file_list:
		filepath = dir + "/" + file
		f = codecs.open(filepath, "r", "utf8")
		title = f.readline()
		date = title[-10:-2]
		date = date[:4] + "/" + date[4:6] + "/" + date[6:]
		title = title.split("	")[0]
		content = f.read()
		intro = content[:50] + "..."
		
		fp = dir.split('\\')[-1] + "/" + file
		news = News(title=title, date=date, content=content, intro=intro, filepath=fp)
		news.save()
		
		f.close()

def target_link(link):
	return True
	#if "20180912" in link:
	#	return True
	#return False

def save_news_model():
	print("hello")
	crawler_dir = os.getcwd()[:-7] + "crawler"
	dir_list = os.listdir(crawler_dir)
	for dir in dir_list:
		if "." in dir or target_link(dir) == False:
			continue
		get_files(crawler_dir + "\\" + dir)

#save_news_model()
save_word_model()
