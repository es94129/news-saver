from django.shortcuts import render
from django.views import generic
from blog.models import News, Word
from django.db.models import Q
from collections import Counter
import time
import jieba

def index(request): #not using, used NewsListView instead
    """View function for home page of site."""

    # Generate counts of some of the main objects
    #num_news = News.objects.all().count()
    
    #context = {
    #    'num_news': num_news,
    #}

    # Render the HTML template index.html with the data in the context variable
    #return render(request, 'index.html', context=context)

    news = []
    newss = News.objects.filter(id__range=(37930, 37941))
    for cur_news in newss:
    	cur_dict = {}
    	cur_dict['title'] = cur_news.title
    	cur_dict['content'] = cur_news.content[:50] + "..."
    	news.append(cur_dict)
    return render(request, 'index.html', {'news':news})

class NewsListView(generic.ListView):
	model = News
	paginate_by = 16

	context_object_name = "news_list"

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(NewsListView, self).get_context_data(**kwargs)
		context['num'] = News.objects.all().count()
		return context

class NewsDetailView(generic.DetailView):
    model = News

    
    def get_context_data(self, **kwargs):
    	context = super(NewsDetailView, self).get_context_data(**kwargs)

    	seg_list = jieba.cut(self.object.content)
    	#tag
    	c = Counter()
    	for x in seg_list:
    		if len(x) > 1 and x != '\r\n':
    			c[x] += 1
    	tags = c.most_common(5)

    	context['tags'] = tags

    	try:
    		context['previous'] = News.objects.get(pk=self.object.pk-1)
    	except:
    		context['previous'] = None
    	try:
    		context['next'] = News.objects.get(pk=self.object.pk+1)
    	except:
    		context['next'] = None
    	return context
	

class NewsSearchListView(NewsListView):
	paginate_by = 16

	def get_queryset(self):
		result = super(NewsSearchListView, self).get_queryset()
		query = self.request.GET.get('s')

		ls = query.split(' ')
		newss = News.objects.filter(title__icontains="陈颖陈颖陈颖")
		date1 = ""
		date2 = ""
		for s in ls:
			if ("[" in s) and ("]" in s):#date
				date1 = s[1:9]
				date1 = date1[:4]+"/"+date1[4:6]+"/"+date1[6:]
				date2 = s[10:-1]
				date2 = date2[:4]+"/"+date2[4:6]+"/"+date2[6:]
				continue
			try:
				word = Word.objects.get(spell=s)
				cur_newss = word.news_set.all()
				if cur_newss.count() == 998:
					cur_newss = News.objects.filter(Q(title__icontains=s)|Q(content__icontains=s))
				newss = newss | cur_newss
			except:
				continue
		for s in ls:
			for new in newss:
				if s in new.title:
					idx = new.title.find(s)
					new.title = new.title[:idx] + "<mark>" + s + "</mark>" + new.title[idx+len(s):]
				if s in new.content:
					idx = new.content.find(s)
					new.intro = new.content[idx-25:idx] + "<mark>" + s + "</mark>" + new.content[idx+len(s):idx+len(s)+25] + "..."
		if date1 != "" and date2 != "":
			newss = newss.filter(date__range=[date1,date2])
			for s in ls:
				for new in newss:
					if s in new.title:
						idx = new.title.find(s)
						new.title = new.title[:idx] + "<mark>" + s + "</mark>" + new.title[idx+len(s):]
					if s in new.content:
						idx = new.content.find(s)
						new.intro = new.content[idx-25:idx] + "<mark>" + s + "</mark>" + new.content[idx+len(s):idx+len(s)+25] + "..."
			return newss
		return newss


	def get_context_data(self, **kwargs):
		query = self.request.GET.get('s')
		context = super(NewsSearchListView, self).get_context_data(**kwargs)

		t_start = time.time()
		ls = query.split(" ")

		newss = News.objects.filter(title__icontains="陈颖陈颖陈颖")
		date1 = ""
		date2 = ""
		for s in ls:
			if ("[" in s) and ("]" in s):#date
					date1 = s[1:9]
					date1 = date1[:4]+"/"+date1[4:6]+"/"+date1[6:]
					date2 = s[10:-1]
					date2 = date2[:4]+"/"+date2[4:6]+"/"+date2[6:]
					continue
			try:
				word = Word.objects.get(spell=s)
				cur_newss = word.news_set.all()
				if cur_newss.count() == 998:
					cur_newss = News.objects.filter(Q(title__icontains=s)|Q(content__icontains=s))
				newss = newss | cur_newss
			except:
				continue
		t_end = time.time()
		context['time'] = "used " + str(t_end - t_start) + " seconds"
		if date1 != "" and date2 != "":
			context['num'] = newss.filter(date__range=[date1,date2]).count()
		else:
			context['num'] = newss.count()
		return context