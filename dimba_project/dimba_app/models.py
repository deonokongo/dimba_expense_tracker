from django.db import models

# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploaded_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
class Savings(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='uploaded_images/', null=True, blank=True)


    def __str__(self):
        return f"{self.name}"
    
class Loan(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploaded_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
class UploadedImage(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploaded_images/')


    def __str__(self):
        return f"{self.title}"
