
from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    CHOICES = (
        ('coming_soon', '即將上映'),
        ('showing', '現正熱映'),
        ('removed','下架電影')
    )
    class Meta:
        model = Movie
        fields = ['date', 'show', 'director', 'actor', 'type', 'length', 'picture', 'movie_name']


class MemberSearchForm(forms.Form):
    member_id = forms.CharField(label='會員编號', max_length=100)

