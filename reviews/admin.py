from django.contrib import admin
from .models import Book, Review, BookShelf


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'rating', 'created_at')  # Используй 'author', а не 'user'
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'text')


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'shelf_type', 'added_date')
    list_filter = ('shelf_type', 'added_date')
    search_fields = ('user__username', 'book__title', 'notes')


admin.site.register(Book)
