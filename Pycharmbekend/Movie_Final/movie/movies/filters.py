from django_filters import FilterSet
from .models import Movie


class MovieFilter(FilterSet):
    class Meta:
        model=Movie
        fields={
            'year': ['gt', 'lt'],
            'country': ['exact'],
            'genre_category': ['exact'],
            'status_movie':['exact'],
            'actor_name': ['exact'],
            'director': ['exact'],

        }

