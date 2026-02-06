from django import forms
from .models import Review, BookShelf


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Напишите ваш отзыв...'}
            ),
            'rating': forms.Select(choices=Review.RATING_CHOICES)
        }


class BookShelfForm(forms.ModelForm):
    class Meta:
        model = BookShelf
        fields = ['shelf_type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Ваши заметки о книге...'
            }),
        }
