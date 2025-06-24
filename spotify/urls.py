from django.urls import path
from . import views


urlpatterns  = [
   path('', views.index, name='index'),
   path('artist/<int:artist_id>', views.artist, name='artist'),
   path('track/<int:track_id>', views.track,name='track' ),
   path('album/<int:album_id>', views.album,name='album' ),
   path('search', views.search, name='search')

   ]