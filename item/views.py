from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

def items(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        items = items.filter(category_id = category_id)
    return render(request, 'item/items.html', {'items': items, 
                                               'query': query, 
                                               'categories': categories,
                                               'category_id': int(category_id)}
                                               )


# Create your views here.
def detail(request, item_id):
    item= get_object_or_404(Item, pk=item_id)
    related_items = Item.objects.filter(category=item.category).exclude(pk=item_id)[:4]
    return render(request, 'item/detail.html', {'item' : item,
                                                'related_items' : related_items,})

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit = False) #commit=False means that it will not save to the database yet
            item.created_by = request.user
            item.save()
            return redirect('item:detail', item_id=item.pk)    
    else:
        form = NewItemForm()
    return render(request, 'item/form.html', {'form': form, 'title': 'New Item'})


@login_required
def delete(request, item_id):
    item = get_object_or_404(Item, pk=item_id, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')


@login_required
def edit(request, item_id):
    item = get_object_or_404(Item, pk=item_id, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item) #instance=item means that it will update the item

        if form.is_valid():
           form.save()
        return redirect('item:detail', item_id=item.id)    
    else:
        form = EditItemForm(instance=item)
        return render(request, 'item/form.html', {'form': form, 'title': 'Edit Item'})

