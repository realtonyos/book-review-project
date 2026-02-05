from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Book, Review
from .forms import ReviewForm



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

    # Получаем все отзывы для этой книги
    all_reviews = book.reviews.all()

    # Настраиваем пагинацию: 5 отзывов на страницу
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-параметра

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не число, показываем первую страницу
        reviews = paginator.page(1)
    except EmptyPage:
        # Если страница пуста, показываем последнюю
        reviews = paginator.page(paginator.num_pages)

    # Остальной код формы остается без изменений
    if request.method == 'POST':
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
        'reviews': reviews,  # Теперь это page object, а не QuerySet
        'form': form
    }
    return render(request, 'reviews/book_detail.html', context)
