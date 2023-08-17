from django.db import models
from django.contrib.auth.models import User #importamos el modelo de usuario de django
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    description = models.TextField(verbose_name='Category description')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Item name')
    description = models.TextField(verbose_name='Item description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Item price', blank=True, null=True)
    image = models.ImageField(upload_to='item_images', verbose_name='Item image', blank=True, null=True)
    is_sold = models.BooleanField(default=False, verbose_name='Is item sold?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at') #django sets time automatically
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE, verbose_name='Created by')
    #models.CASCADE lo que hace es que si se borra el usuario, se borra el item del usuario
    category = models.ForeignKey(Category, related_name='items' , on_delete=models.CASCADE, verbose_name='Item category')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name']
    def __str__(self):
        return self.name