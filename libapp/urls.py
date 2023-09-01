from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('issue/<int:book_id>/<int:member_id>/', views.issue_book, name='issue_book'),
    path('issue_book/', views.issue_book, name='issue_book'),

    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('search/', views.search_books, name='search_books'),
    path('import/', views.import_books, name='import_books'),
    path('members/', views.member_list, name='member_list'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    path('add_member/', views.add_member, name='add_member'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]
