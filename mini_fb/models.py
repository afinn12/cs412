from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of a Facebook Profile'''

    # every Profile has one User:
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    
    def get_friends(self):
        '''Return a list of profiles that are friends with this profile.'''

        # Retrieve Friend instances where this profile is either profile1 or profile2
        profile1 = Friend.objects.filter(profile1=self)
        profile2 = Friend.objects.filter(profile2=self)

        # Collect all the friend profiles (either from profile1 or profile2)
        friend_profiles = [
            friend.profile2 for friend in profile1
        ] + [
            friend.profile1 for friend in profile2
        ]

        return friend_profiles
    
    def add_friend(self, other):
        """Add a friendship if it doesn't already exist and is not self-friending."""
        if self == other:
            raise ValueError("You cannot add yourself as a friend.")

        existing = Friend.objects.filter(
            profile1=self, profile2=other
        ) | Friend.objects.filter(
            profile1=other, profile2=self
        )

        if existing:
            raise ValueError("Friendship already exists.")

        # Create the new Friend relationship
        Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        '''Return a list of possible friends for this profile.'''
        # Get all friends of the current profile
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        friends = list(friends1) + list(friends2)

        # Get all profiles that are not friends and not the current profile
        friend_suggestions = Profile.objects.exclude(
            id__in=friends  # Exclude current friends
        ).exclude(
            id=self.id      # Exclude the current profile
        )

        return friend_suggestions
    

    def get_news_feed(self):
        '''Return a combined list of status messages for this profile and its friends.'''
        # Get the current profile's status messages
        own = StatusMessage.objects.filter(profile=self)

        # Get the friends of this profile
        friends = self.get_friends() 

        # Get status messages from friends
        other = StatusMessage.objects.filter(profile__in=friends)

        # Combine own messages and friends' messages
        all_messages = own | other

        # Return combined messages sorted by timestamp (most recent first)
        return all_messages.order_by('-timestamp')



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
    '''Encapsulate the idea of an Image on a StatusMessage.'''

    status = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.image_file}'
        
class Friend(models.Model):
    '''Encapsulate the idea of a friendship between two Profiles.'''
    
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        '''Return a string representation of this Friend object.'''
        return f'{self.profile1.first} {self.profile1.last} & {self.profile2.first} {self.profile2.last}'

    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        return reverse('friendship_detail', kwargs={'pk': self.pk})


