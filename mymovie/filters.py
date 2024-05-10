from .models import Movie,Member_data
import django_filters

class MovieFilter(django_filters.FilterSet):


    class Meta:
        model = Movie
        fields = '__all__'


class MemberFilter(django_filters.FilterSet):
    member_account = django_filters.CharField(max_length=200)

    class Meta:
        model = Member_data
        fields = '__all__'
