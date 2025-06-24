import os
import requests


JAMENDO_ENDPOINTS = {
    'artist_api': 'https://api.jamendo.com/v3.0/artists',
    'tracks_api': 'https://api.jamendo.com/v3.0/tracks',
    'albums_api': 'https://api.jamendo.com/v3.0/albums'
}


def get_top_artists_service():
    #CALLS JAMENDO API
    
    params = {
        "client_id": os.environ.get('JAMENDO_CLIENT'),
        "format": "json",
        "limit": 14,
        "order": "popularity_week" 
    }                
    
    try:
        response = requests.get(JAMENDO_ENDPOINTS['artist_api'], params)
        response.raise_for_status()
        results = response.json().get('results',[])
        if results:
            return results
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jamendo API: {e}")
        return None            

def get_artist_service(artist_id):
    
    params = {
        "client_id": os.environ.get('JAMENDO_CLIENT'),
        "format":"json",
        "id": artist_id
    }
    
    try:
        response = requests.get(JAMENDO_ENDPOINTS['artist_api'], params)
        response.raise_for_status()
        results = response.json().get('results',[])
        if results:
            return results
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jamendo API: {e}")
        return None         
            
def get_top_albums_service():        
    params = {        
        "client_id":os.environ.get('JAMENDO_CLIENT'),
        "format":"json",
        "limit":10,
        "order":"popularity_week"
    }
    
    try:
        response = requests.get(JAMENDO_ENDPOINTS['albums_api'], params)
        response.raise_for_status()
        results = response.json().get('results',[])
        if results:
            return results
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jamendo API: {e}")
        return None         
    
    
def get_artist_details(artist_id):
    params = {        
        "client_id":os.environ.get('JAMENDO_CLIENT'),
        "format":"json",        
        "order":"popularity_week",
        "artist_id":artist_id
    }
    #Fetch all albums for this artist
    try:
        response = requests.get(JAMENDO_ENDPOINTS['albums_api'], params)        
        albums = response.json().get('results', [])
        
    #fetch top 10 tracks 
        params['limit'] = 10
        params['include'] = 'stats'
        response = requests.get(JAMENDO_ENDPOINTS['tracks_api'], params)    
        top_tracks = response.json().get('results', [])    
        return(albums, top_tracks)
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jamendo API: {e}")
        return(None, None)


def get_track(track_id):
    params= {
        "client_id":os.environ.get('JAMENDO_CLIENT'),
        "format":"json",
        "id": track_id
    }
    
    try:
        response = requests.get(JAMENDO_ENDPOINTS['tracks_api'], params)
        response.raise_for_status()
        results = response.json().get('results',[])
        if results:
            #result is always an array so we return always the first index 
            return results[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        
        print(f"Error calling Jamendo API: {e}")
        return None  

def get_tracks_by_album(album_id):
    params = {
        "client_id":os.environ.get('JAMENDO_CLIENT'),
        "format":"json",
        "album_id": album_id
    }
    
    try:
        response = requests.get(JAMENDO_ENDPOINTS['tracks_api'], params)
        response.raise_for_status()
        results = response.json().get('results',[])
        if results:
            return results
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jamendo API: {e}")
        return None  


def search(keyword, page):
    #1- find tracks
    offset = 0
    if page and page > 0:
        offset = 20*page
    
    params = {
        "client_id":os.environ.get('JAMENDO_CLIENT'),
        "format":"json",
        "search": keyword,
        "limit": 20,
        "offset": offset
    }

    
    response_tracks = requests.get(JAMENDO_ENDPOINTS['tracks_api'], params)
    
    tracks = response_tracks.json().get('results', [])
    
    #2 - Find Artists
    response_artists = requests.get(JAMENDO_ENDPOINTS['artist_api'], params)    
    
    artists = response_artists.json().get('results', [])
    print(artists)
    
    #3 - Find Albums
    response_albums = requests.get(JAMENDO_ENDPOINTS['albums_api'], params)
    
    albums = response_albums.json().get('results', [])
    
    return tracks, artists, albums