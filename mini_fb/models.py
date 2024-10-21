from django.db import models
from django.urls import reverse

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
        '''Return all of the statusmessages about this profile.'''
        statusmessages = StatusMessage.objects.filter(profile=self)
        return statusmessages

    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('profile', kwargs={'pk': self.pk})

 
class StatusMessage(models.Model):
    '''Encapsulate the idea of a StatusMessage on a Profile.'''
    
    # data attributes of a Comment:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all of the statusmessages about this article.'''
        image = Image.objects.filter(status=self)
        return image
    
    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('profile', kwargs={'pk': self.profile.pk})

class Image(models.Model):
    status = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.image_file}'
        