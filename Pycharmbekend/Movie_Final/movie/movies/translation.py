from .models import *
from modeltranslation.translator import TranslationOptions,register


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('movie_name', 'description')


@register(Director)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('director_name', 'bio')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('Actor_name', 'bio')


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)