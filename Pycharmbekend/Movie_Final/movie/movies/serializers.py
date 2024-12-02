from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['username', 'email', 'password', 'first_name','last_name',
                'age','phone_number','account_type',]
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh=RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['username']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=['country_name']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['Actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language','video']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'



class MovieListSerializer(serializers.ModelSerializer):
    country=CountrySerializer(many=True)
    genre_category=GenreSerializer(many=True)
    year=serializers.DateField(format('%d-%m-%Y'))
    avg_rating=serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['id','movie_name','year',
                  'country','genre_category','status_movie','avg_rating']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    genre_category = GenreSerializer(many=True)
    year = serializers.DateField(format('%d-%m-%Y'))
    actor_name=ActorListSerializer(many=True)
    director=DirectorListSerializer(many=True)
    Movie_language=MovieLanguagesSerializer(many=True,read_only=True)
    moments=MomentsSerializer(many=True,read_only=True)
    class Meta:
        model = Movie
        fields = ['movie_name','year','country',
                  'director','actor_name','genre_category',
                  'types','movie_time','description',
                  'movie_trailer','movie_image','status_movie','Movie_language','moments']


class DirectorDetailSerializer(serializers.ModelSerializer):
    director=MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Director
        fields = ['director_name','bio','age','director_image','director']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_movie=MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Actor
        fields = ['Actor_name','bio','age','Actor_image','actor_movie']