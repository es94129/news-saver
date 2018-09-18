from django.urls import path
from blog import views
import re
urlpatterns = [
	#path('', views.index, name='index'),
	path('',views.NewsListView.as_view(),name='news-list'),
	path('article/<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
	path('search/',views.NewsSearchListView.as_view(), name='news-search')
]