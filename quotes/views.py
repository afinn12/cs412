## quotes/views.py
## description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

#Create your views here.

people = ["Alan Turing", "Bill Gates", "Snoop Dogg", "Ron Jeffries", "Linus Torvalds"]
pics = ["https://tinyurl.com/2xr4hejb", 
        "https://i.insider.com/56a6896bdd0895ad088b477a?width=1000&format=jpeg", 
        "https://tinyurl.com/snoopdogpfp", 
        "https://pbs.twimg.com/profile_images/1072295406355259393/Hqsx90JU_400x400.jpg", 
        "https://media.newyorker.com/photos/5ba177da9eb2f7420aadeb98/4:3/w_1229,h_921,c_limit/Cohen-Linus-Torvalds.jpg"]

words = ["We can only see a short distance ahead, but we can see plenty there that needs to be done.", 
         "The computer was born to solve problems that did not exist before.",
         "support tha american dream n make coding available to EVERYONE!!",
         "Code never lies, comments sometimes do.",
         "Nobody actually creates perfect code the first time around, except me. But there's only one of me."]

def main(request):
    '''
    Function to handle the URL request for /quotes (home page).
    Delegate rendering to the template quotes/main.html.
    '''
    # use this template to render the response
    template_name = 'quotes/quote.html'

    r = random.randint(0,4)
    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "name" : people[r], # a letter from A ... Z
        "pic" : pics[r], # a letter from A ... Z
        "word" : words[r], # number frmo 1 to 10
    }

    # delegate rendering work to the template
    return render(request, template_name, context)


def quote(request):
    '''
    Function to handle the URL request for /quotes/quote (quote page).
    Delegate rendering to the template quotes/quote.html.
    '''
     # use this template to render the response
    template_name = 'quotes/quote.html'

    r = random.randint(0,4)
    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "name" : people[r], # a letter from A ... Z
        "pic" : pics[r], # a letter from A ... Z
        "word" : words[r], # number frmo 1 to 10
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def showall(request):
    '''
    Function to handle the URL request for /quotes/show_all (showall page).
    Delegate rendering to the template quotes/show_all.html.
    '''
    # use this template to render the response
    template_name = 'quotes/show_all.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "people" : people,
        "pics" : pics,
        "words" : words
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /quotes/about (about page).
    Delegate rendering to the template quotes/about.html.
    '''
    # use this template to render the response
    template_name = 'quotes/about.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "people" : people,
        "pics" : pics,
    }

    # delegate rendering work to the template
    return render(request, template_name, context)