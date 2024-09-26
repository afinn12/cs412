
from django.shortcuts import render, redirect
import time, random
# Create your views here.

food = ['Birria Tacos', 'Carne Asada Tacos', 'Al Pastor Tacos', 'Carnitas Tacos', 'Vegetarian tacos', 'Chorizo Tacos', 'Pescado Tacos']



def show_main(request):
    ''' Show the main page for the restaurant'''
    
    template_name = "restaurant/main.html"

    context = {
        "current_time" : time.ctime()
    }

    return render(request, template_name, context)


def show_order(request):
    '''Show the page to order'''

    template_name = "restaurant/order.html"

    t = time.localtime()

    context = {
        "special" : food[t.tm_wday],
        "current_time" : time.ctime()
    }


    return render(request, template_name, context)

def show_confirmation(request):
    '''
    Handle the form submission.
    Read the form data from the request,
    and send it back to a template.
    '''

    template_name = 'restaurant/confirmation.html'
    # print(request)
    
    # check that we have a POST request
    if request.POST:

        # print(request.POST)
        # read the form data into python variables
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        bowl_protein = request.POST['bowl-protein']
        burrito_protein = request.POST['burrito-protein']
        food = request.POST.getlist('food')

        special = request.POST['special']

        min = random.randint(30, 60)

      
        # Calculate the total cost based on the order
        total = 0
        for f in food:
            if (f == 'Burrito'):
                total += 9
            if (f == 'Bowl'):
                total += 9
            if (f == 'Quesadilla'):
                total += 6
            if (f == 'Chips & Gauc'):
                total += 4
            if ('Tacos' in f):
                total += 10
            
        # Account for tax
        total *= 1.1

        

        # package the form data up as context variables for the template
        context = {
            "current_time" : time.ctime(),
            'readytime' : time.ctime(time.time()+ min*60),
            'name' : name,
            'phone' : phone,
            'email' : email,
            'food' : food,
            'special' : special,
            'bowl_protein' : bowl_protein,
            'burrito_protein' : burrito_protein,
            'total' : "{:.2f}".format(total),
        }

        return render(request, template_name, context)
    
    ## handle GET request on this URL
    # an "ok" solution...
    # return HttpResponse("Nope.")

    ## a "better" solution...
    # template_name = "restaurant/form.html"
    # return render(request, template_name)
    
    # an even better solution: redirect to the correct URL:
    return redirect("show_order")