from rest_framework import routers
from .views import *
from django.urls import path, include


router=routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user' )
router.register(r'director', DirectorListViewSet, basename='director_list' )
router.register(r'director_detail', DirectorDetailViewSet, basename='director_detail')
router.register(r'actor_list', ActorListViewSet, basename='actor_list' )
router.register(r'actor_detail', ActorDetailViewSet, basename='actor_detail' )
router.register(r'favorite', FavoriteViewSet, basename='favorite' )
router.register(r'favorite_movie', FavoriteMovieViewSet, basename='favorite_movie' )
router.register(r'history', HistoryViewSet, basename='history' )
router.register(r'rating', RatingViewSet, basename='rating' )

urlpatterns = [
    path('',include(router.urls)),
    path('movie/', MovieListApiView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailApiView.as_view(), name='movie_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]



