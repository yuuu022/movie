
from django import forms
from .models import Movie, Member_data


class MovieForm(forms.ModelForm):
    CHOICES = (
        ('coming_soon', '即將上映'),
        ('showing', '現正熱映'),
        ('removed','下架電影')
    )
    class Meta:
        model = Movie
        fields = ['date', 'show', 'director', 'actor', 'type', 'length', 'picture', 'movie_name']

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member_data
        fields = ['member_password','gmail','phone_number']



class MemberSearchForm(forms.Form):
    member_id = forms.CharField(label='會員编號', max_length=100)

