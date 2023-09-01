from django.contrib import admin
from .models import Book, Member, Transaction

# Register your models with the admin site
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publisher', 'page_count', 'stock')
    list_filter = ('author', 'publisher')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name',)  

    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'return_date', 'fee')
    list_filter = ('issue_date', 'return_date')
    search_fields = ('book__title', 'member__name', 'book__isbn')  
