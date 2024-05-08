
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['movie_name', 'date', 'show', 'director', 'actor', 'type', 'length', 'picture', 'change_staff']

