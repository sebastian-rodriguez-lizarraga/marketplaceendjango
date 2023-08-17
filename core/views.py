from django.shortcuts import render,redirect

from item.models import Category, Item 
from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold = False).order_by('-created_at')[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'items': items,
        'categories': categories,    
        }) 
    #render is a function that takes in a request and a template name and returns a response 

def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            #create user
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})
