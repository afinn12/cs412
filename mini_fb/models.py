from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a Facebook Profile'''

    # data attributes of a Profile:
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first} {self.last}'
