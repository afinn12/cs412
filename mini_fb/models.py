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
    
    def get_statusmessages(self):
        '''Return all of the statusmessages about this article.'''
        statusmessages = StatusMessage.objects.filter(profile=self)
        return statusmessages

 
class StatusMessage(models.Model):
    '''Encapsulate the idea of a StatusMessage on a Profile.'''
    
    # data attributes of a Comment:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.message}'
       