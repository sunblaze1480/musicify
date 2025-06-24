from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import services
from .utils.mem_cache import add_to_cache


# Custom functions import
from .utils.session_cache import add_to_session_cache

# Create your views here.
@login_required(login_url='login')
def index(request):
    
    top_artists = services.get_top_artists_service()
    top_albums = services.get_top_albums_service()   
            
    context = {
        'top_artists' : top_artists,
        'top_albums' : top_albums
    }
    
    
    return render(request, 'index.html', context)

@login_required(login_url='login')
def artist(request, artist_id):
    name = request.GET.get('name')
    image = request.GET.get('image')        
    
    albums, top_tracks = services.get_artist_details(artist_id)
    
    if not name or not image:
        cache_key=f"jamendo:artists:{artist_id}"
        #get from session cache        
        # artist = request.session.get('jamendo',{}).get('artists',{}).get(artist_id)        
        artist = cache.get(cache_key)
        
        #if not on session cache retrieve from API
        if not artist:
            artist = services.get_artist_service(artist_id)
        pass
    else:
        artist = {
            'name' : name,
            'image' : image,
        }
    
    #add artist data to session cache
    add_to_session_cache(request.session, "artists", artist_id, artist, max_items=10)
    
    for track in top_tracks:
         add_to_session_cache(request.session, "tracks", track["id"], track, max_items=10)
                    
    context = {
        'albums': albums,
        'top_tracks': top_tracks,
        'name': name,
        'image': image
    }
    
    return render(request, 'artist.html', context)

@login_required(login_url='login')
def track(request, track_id):
    #check if track is in cache
    cache_key= f"jamendo:tracks:{track_id}"
    track = cache.get(cache_key)    
    
    if not track:
        print("NOT TRACK, GET FROM SERVICE")
        t = services.get_track(track_id)
        if t:
            track = t[0]
        else: 
            track = {
                'name':'Not Found',
                'artist_id': '0',                
            }
    else:
        print(f"retrieved from cache {track_id}")
            
    #add_to_session_cache(request.session, "tracks", track_id, track, max_items=10)
    add_to_cache("tracks", track_id, track, max_items=100)
    
    context = {
        'track': track                
    }
    
    return render(request, 'track.html', context)

@login_required(login_url='login')
def album(request, album_id):
    
    cache_key = f"jamendo:albums:{album_id}"    
    tracklist = cache.get(cache_key)        
    if not tracklist:
        tracklist = services.get_tracks_by_album(album_id)
    else:
        print(f"retrieved from cache {album_id}")
                    
    add_to_cache("albums", album_id, tracklist, max_items=100)
            
    album_metadata = {
        'album_image': tracklist[0]['album_image'] if tracklist else None,
        'album_name': tracklist[0]['album_name']  if tracklist else None,
        'artist_name': tracklist[0]['artist_name']  if tracklist else None,
        'artist_id' : tracklist[0]['artist_id']  if tracklist else None,
    }

    context = {
        'album_metadata' : album_metadata,
        'tracklist' : tracklist
    }
        
    return render(request, 'album.html', context)

@login_required(login_url='login')
def search(request):
    
    keyword = request.GET.get('keyword')
    page = request.GET.get('page')
    
    if not keyword: 
        messages.info(request, 'Please enter something to search')
        return redirect('index')
    
    if not page:
        page = 0
    
    tracks, artist, albums = services.search(keyword, page)
            
    context = { 
        'tracks': tracks,
        'artist': artist,
        'albums': albums,
        'keyword' : keyword
    }
    
    return render(request, 'search.html', context)