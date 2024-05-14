from .models import Movie,Member_data
import django_filters
from django import forms

class MovieFilter(django_filters.FilterSet):
    movie_name = django_filters.CharFilter(
        field_name='movie_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = django_filters.CharFilter(
        field_name='date',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    type= django_filters.CharFilter(
        field_name='type',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Movie
        fields = '__all__'


class MemberFilter(django_filters.FilterSet):

    class Meta:
        model = Member_data
        fields = '__all__'