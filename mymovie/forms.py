
from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['date', 'show', 'director', 'actor', 'type', 'length', 'picture', 'change_staff', 'movie_name']


class MemberSearchForm(forms.Form):
    member_id = forms.CharField(label='會員编號', max_length=100)

