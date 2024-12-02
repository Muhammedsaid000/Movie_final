from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


STATUS_CHOICES = (
    ('pro', 'Pro'),
    ('simple', 'Simple'),
)


class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(70)])
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    account_type = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Country(models.Model):
   country_name=models.CharField(max_length=40, unique=True)

   def __str__(self):
       return self.country_name


class Director(models.Model):
    director_name=models.CharField(max_length=20)
    bio=models.TextField()
    age=models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    director_image=models.ImageField(upload_to='director_img/',verbose_name='image',)

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    Actor_name = models.CharField(max_length=20)
    bio = models.TextField()
    age=models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    Actor_image = models.ImageField(upload_to='actor_img/', verbose_name='image', )

    def __str__(self):
        return self.Actor_name


class Genre(models.Model):
    genre_name=models.CharField(max_length=20)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name=models.CharField(max_length=100)
    year=models.DateField()
    country=models.ManyToManyField(Country,)
    director=models.ManyToManyField(Director, related_name='director')
    actor_name=models.ManyToManyField(Actor, related_name='actor_movie')
    genre_category=models.ManyToManyField(Genre,  related_name='genre')
    TYPES_CHOICES = (
        ('144', '144'),
        ('360', '360'),
        ('480', '480'),
        ('720', '720'),
        ('1080', '1080'),
    )
    types = MultiSelectField(choices=TYPES_CHOICES, max_length=100,max_choices=15)
    movie_time=models.PositiveSmallIntegerField(default=1)
    description=models.TextField()
    movie_trailer=models.FileField(upload_to='movie_trailer/', verbose_name='movie_video')
    movie_image=models.ImageField(upload_to='movie_img/',verbose_name='movie_image')
    status_movie=models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.movie_name

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum(i.starts for i in ratings) / ratings.count(),1)
        return 0


class MovieLanguages(models.Model):
    language=models.CharField(max_length=30)
    video=models.FileField(upload_to='languages_vid/')
    movie=models.ForeignKey(Movie,related_name='Movie_language',on_delete=CASCADE)

    def __str__(self):
        return self.language

class Moments(models.Model):
    movie=models.ForeignKey(Movie, related_name='moments',on_delete=CASCADE)
    movie_moments=models.ImageField(upload_to='moments_img/',verbose_name='image')


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE, related_name='reviews')
    starts = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], verbose_name="Рейтинг",null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    parent_review=models.ForeignKey('self',null=True, blank=True , on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, related_name='items', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
