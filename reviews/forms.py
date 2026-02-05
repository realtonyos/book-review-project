from django import forms
from .models import Review


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
