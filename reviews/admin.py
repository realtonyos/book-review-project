from django.contrib import admin
from .models import Book, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'rating', 'created_at')  # Используй 'author', а не 'user'
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'text')


admin.site.register(Book)
