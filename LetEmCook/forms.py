from django import forms
from .models import Recipe, Comment, Profile
from django.contrib.auth.models import User

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'description', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'ingredients': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input ingredients (comma-separated) | ingredient1, ingredient2, ingredient3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input recipe description and instructions'}), 
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input tags (comma-separated) | tag1, tag2, tag3'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment something'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class EmailMFAForm(forms.Form):
    code = forms.CharField(max_length=6, label='Enter the code sent to your email')
