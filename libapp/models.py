from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=100)
    page_count = models.IntegerField()
    stock = models.IntegerField(default=0)

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,null=True,blank=True)


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)




