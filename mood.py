import json
import requests
from random import shuffle
from settings import *
from pprint import pprint

def get_top_artists(auth_header, num_entities):
    """ Return list of user's top and followed artists """

    artists = []

    term = ['long_term', 'short_term']

    for length in term:
        request = f'{SPOTIFY_API_URL}/me/top/artists?time_range={length}&limit={num_entities}'
        top_artists_data = requests.get(request, headers=auth_header).json()
        top_artists = top_artists_data['items']
        for top_artist in top_artists:
            if top_artist['id'] not in artists:
                artists.append(top_artist['id'])

    users_followed_artists = f'{SPOTIFY_API_URL}/me/following?type=artist&limit={num_entities}'
    followed_artists_data = requests.get(users_followed_artists, headers=auth_header).json()

    followed_artists = followed_artists_data['artists']['items']

    for followed_artist in followed_artists:
        if followed_artist['id'] not in artists:
            artists.append(followed_artist['id'])

    return artists


def get_related_artists(auth_header, top_artists):
    """ Return list of related artists using users top artist """

    new_artists = []

    for artist_id in top_artists[:1]:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/related-artists'
        related_artists_data = requests.get(request, headers=auth_header).json()
        related_artists = related_artists_data['artists']

        for related_artist in related_artists:
            if related_artist['id'] not in new_artists:
                new_artists.append(related_artist['id'])

    artists = set(top_artists + new_artists)

    return artists

def get_top_tracks(auth_header, artists):
    """ Get top tracks of artists """

    top_tracks = []

    for artist_id in artists:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks?country=US'
        track_data = requests.get(request, headers=auth_header).json()
        tracks = track_data['tracks']

        for track in tracks:
            if track['id'] not in top_tracks:
                top_tracks.append(track['id'])

    return top_tracks

def cluster_ids(tracks, n = 100):
    """ Return list of track ids clustered in groups of 100 """
    
    shuffle(tracks)

    clustered_tracks = []
    for i in range(0, len(tracks), n):
        clustered_tracks.append(tracks[i:i + n])

    return clustered_tracks


def select_tracks(auth_header, clustered_tracks, mood):
    """ Select tracks based on user's mood """

    selected_tracks = []

    for track_ids in clustered_tracks:
        ids = '%2C'.join(track_ids)
        request = f'{SPOTIFY_API_URL}/audio-features?ids={ids}'
        audio_features_data = requests.get(request, headers=auth_header).json()
        audio_features = audio_features_data['audio_features']

    # Below is not selecting the correct tracks
    #     for track in audio_features:
    #         if mood <= 0.10:
    #             if (track['danceability'] <= 0.10) and (track['energy'] <= 0.20) and (track['valence'] <= 0.10):
    #                 selected_tracks.append(track['id'])
    #         elif mood <= 0.25:
    #             if (0.10 < track['danceability'] <= 0.25) and (0.20 < track['energy'] <= 0.30) and (0.10 < track['valence'] <= 0.20):
    #                 selected_tracks.append(track['id'])
    #         elif mood <= 0.50:
    #             if (0.25 < track['danceability'] <= 0.05) and (0.30 < track['energy'] <= 0.40) and (0.20 < track['valence'] <= 0.40):
    #                 selected_tracks.append(track['id'])
    #         elif mood <= 0.75:
    #             if (0.50 < track['danceability'] <= 0.75) and (0.40 < track['energy'] <= 0.50) and (0.50 < track['valence']):
    #                 selected_tracks.append(track['id'])
    #         elif mood <= 0.90:
    #             if (0.75 < track['danceability'] <= 0.9) and (0.50 < track['energy'] <= 0.70) and (0.50 < track['valence']):
    #                 selected_tracks.append(track['id'])
    #         elif mood <= 1.00:
    #             if (track['danceability'] > 0.9) and (track['energy'] > 0.7) and (0.50 < track['valence']):
    #                 selected_tracks.append(track['id'])

    # return selected_tracks

def create_playlist(auth_header, selected_tracks):
    """ Creates playlist based on mood """

    pass
    




