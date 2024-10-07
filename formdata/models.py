from django.db import models

# Create your models here.

class Article:
    '''Encapsulate the idea of one Article by some author'''
    
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(blank=True)