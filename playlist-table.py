#!/usr/bin/env python3

# Amber Jennings, 2023 ~ https://github.com/amberjennings

import spotipy
import tkinter as tk
import yaml
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from tabulate import tabulate

def load_credentials():
    with open("rb.cfg", "r") as config_file:
        config = yaml.load(config_file, Loader = yaml.FullLoader)
        return config.get("client_id"), config.get("client_secret")

CLIENT_ID, CLIENT_SECRET = load_credentials()
client_credentials_manager = SpotifyClientCredentials(
    client_id = CLIENT_ID, client_secret = CLIENT_SECRET
)
sp = Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_info(playlist_url):
    try:
        results = sp.playlist(playlist_url)
        tracks = results["tracks"]["items"]
        playlist_name = results["name"]
    except spotipy.SpotifyException as e:
        print(f"Error retrieving playlist: {e}")
        return []

    track_info = []
    for track in tracks:
        song_name = track["track"]["name"]
        artists = ", ".join([artist["name"] for artist in track["track"]["artists"]])
        album = track["track"]["album"]["name"]
        duration_ms = track["track"]["duration_ms"]
        duration_min_sec = divmod(duration_ms // 1000, 60)
        length = f"{duration_min_sec[0]:02}:{duration_min_sec[1]:02}"
        track_info.append([song_name, artists, album, length])

    return track_info, playlist_name

def show_table():
    playlist_url = entry.get()
    track_info, playlist_name = get_playlist_info(playlist_url)
    headers = ["Song", "Artist(s)", "Album", "Length"]
    table_data = tabulate(track_info, headers, tablefmt = "github")

    result_window = tk.Toplevel(root)
    result_window.title(playlist_name)

    table_label = tk.Label(
        result_window, text = table_data, font = ("Courier", 14), justify = "left"
    )
    table_label.pack(padx = 10, pady = 10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spotify Playlist Table Creator")

    label = tk.Label(root, text = "Enter Spotify Playlist URL:")
    label.pack(pady = 10)

    entry = tk.Entry(root, width=40)
    entry.pack(pady = 10)

    button = tk.Button(root, text = "Show Playlist", command = show_table)
    button.pack(pady = 10)

    root.mainloop()

