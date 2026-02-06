from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Book, Review, BookShelf
from .forms import ReviewForm, BookShelfForm



def home(request):
    """Главная страница со списком всех книг и поиском"""
    books = Book.objects.all().order_by('-id')

    # Получаем поисковый запрос из GET-параметра
    search_query = request.GET.get('search', '')

    if search_query:
        # Фильтруем книги по названию ИЛИ автору (регистр-независимо)
        books = books.filter(
            models.Q(title__icontains=search_query) | 
            models.Q(author__icontains=search_query)
        )

    context = {
        'books': books,
        'search_query': search_query,  # Передаем запрос в шаблон
    }
    return render(request, 'reviews/home.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    all_reviews = book.reviews.all()

    # Пагинация
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('page', 1)

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    # Обработка формы отзыва
    form = None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Требуется войти в систему, чтобы оставить отзыв.')
            return redirect('users:login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.author = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('reviews:book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
        'user_can_review': request.user.is_authenticated,
        'shelf_form': BookShelfForm(),
        'user_shelves': BookShelf.objects.filter(
            user=request.user,
            book=book
        ) if request.user.is_authenticated else [],
    }
    return render(request, 'reviews/book_detail.html', context)


@login_required
def add_to_shelf(request, book_id):
    """Add book to user's shelf."""
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookShelfForm(request.POST)
        if form.is_valid():
            shelf = form.save(commit=False)
            shelf.user = request.user
            shelf.book = book

            # Удаляем старую запись если есть такой же тип полки
            BookShelf.objects.filter(
                user=request.user, 
                book=book, 
                shelf_type=shelf.shelf_type
            ).delete()

            shelf.save()
            messages.success(request, f'Книга добавлена на полку "{shelf.get_shelf_type_display()}"')

    return redirect('reviews:book_detail', book_id=book.id)
