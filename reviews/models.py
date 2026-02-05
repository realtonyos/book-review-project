from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    genre = models.CharField(max_length=50, verbose_name="Жанр")
    published_year = models.IntegerField(verbose_name="Год издания", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Review(models.Model):
    # Связь с книгой: один ко многим (одна книга - много отзывов)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    # Связь с пользователем: один пользователь - много отзывов
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    # Текст отзыва
    text = models.TextField(verbose_name='Текст отзыва')
    # Оценка от 1 до 5
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=3, 
        verbose_name='Оценка'
    )
    # Дата создания (автоматически при создании)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Новые отзывы первыми

    def __str__(self):
        return f"Отзыв от {self.author} на {self.book.title}"
