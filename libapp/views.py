import requests
from django.shortcuts import render, redirect
from .models import Book
from django.http import HttpResponse


from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Transaction
from django.http import HttpResponse
from datetime import datetime

from django.shortcuts import render, redirect
from .models import Book, Member, Transaction
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Book, Member, Transaction
from django.contrib import messages


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'book_detail.html', {'book': book})




def issue_book(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        book_id = request.POST.get('book_id')
        
        try:
            member = Member.objects.get(pk=member_id)
            book = Book.objects.get(pk=book_id)
            
            if book.id > 0:
                transaction = Transaction(member=member, book=book)
                transaction.save()
                
                book.stock -= 1
                book.save()
                
                messages.success(request, f"Book '{book.title}' issued to {member.name}.")
            else:
                messages.error(request, f"Book '{book.title}' is not available.")
        except Member.DoesNotExist:
            messages.error(request, "Member not found.")
        except Book.DoesNotExist:
            messages.error(request, "Book not found.")
    
    members = Member.objects.all()
    books = Book.objects.all()  
    
    return render(request, 'issue_book.html', {'members': members, 'books': books})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, f"Transaction {transaction_id} has been deleted successfully.")
        return redirect('transaction_list')

    return render(request, 'delete_transaction.html', {'transaction': transaction})


def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == 'POST':
        return_date_str = request.POST.get('return_date')
        if return_date_str:
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()  
            transaction.return_date = return_date
            transaction.save()

            if transaction.return_date > transaction.issue_date:
                days_late = (transaction.return_date - transaction.issue_date).days
                late_fee = days_late * 1.00  
                transaction.late_fee = late_fee
                transaction.save()

                messages.success(request, f"Book '{transaction.book.title}' has been returned with a late fee of Rs. {late_fee:.2f}.")
            else:
                messages.success(request, f"Book '{transaction.book.title}' has been returned.")
        else:
            messages.error(request, "Please provide a return date.")

        return redirect('transaction_list')

    return render(request, 'return_book.html', {'transaction': transaction})
 

def search_books(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
        return render(request, 'library/search_results.html', {'books': books})
    return render(request, 'search_books.html')


def import_books(request):
    if request.method == 'POST':
        num_books_to_import = int(request.POST.get('num_books_to_import', 0))

        title = request.POST.get('title', '')
        authors = request.POST.get('authors', '')
        isbn = request.POST.get('isbn', '')
        publisher = request.POST.get('publisher', '')
        page = request.POST.get('page', '')

        api_url = 'https://frappe.io/api/method/frappe-library?page=2'
        params = {
            'title': title,
            'authors': authors,
            'isbn': isbn,
            'publisher': publisher,
            'page': page,
        }

        headers = {
            'Authorization': 'Bearer your_api_key_here',
        }

        try:
            response = requests.get(api_url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json().get('message', [])

                for book_data in data[:num_books_to_import]:
                    num_pages = book_data.get('num_pages', 0)

                    book = Book(
                        title=book_data['title'],
                        author=book_data['authors'],
                        isbn=book_data['isbn'],
                        publisher=book_data['publisher'],
                        page_count=num_pages,
                    )
                    book.save()

                return redirect('book_list')  
            else:
                error_message = "Failed to fetch data from the API."
                return render(request, 'library/error.html', {'error_message': error_message})

        except Exception as e:
            error_message = str(e)
            return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'import_books.html')



def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def member_detail(request, member_id):
    member = Member.objects.get(pk=member_id)
    return render(request, 'member_detail.html', {'member': member})

def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        member = Member(name=name, email=email)
        member.save()
        return redirect('member_list')  

    return render(request, 'add_member.html')


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})

def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

def home(request):
    return render(request,'home.html')