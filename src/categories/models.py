from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='categories', default='no_picture.png') 
    expense = models.FloatField(help_text='in Indian Rupees')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}-{self.created.strftime('%D/%M/%Y')}"