from django.db import models
from django.urls import reverse

class News(models.Model):

    # Fields
    title = models.CharField(max_length=60, help_text='Title')
    date = models.CharField(max_length=15, help_text='YYYYMMDD') #DateField
    content = models.TextField(null=True, blank = True, help_text = 'Content')
    intro = models.CharField(max_length=55, null=True, blank=True)
    filepath = models.CharField(max_length=30)
    words = models.ManyToManyField('Word')
    #ForeignKey - recommendation

    # Metadata
    class Meta: 
        ordering = ['-date']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('news-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title


class Word(models.Model):
	spell = models.CharField(max_length=20,blank=True,null=True)
	#newss = models.ManyToManyField(News, help_text="The news that use this word.")
	#title = models.CharField(max_length=200)
	#author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	#genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
	#language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.spell