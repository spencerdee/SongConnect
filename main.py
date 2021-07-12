import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = 'a2c8847008ca4c91857343c9cdf22ccb'
secret = '8cf1001a3b5e4ef29b0c5a3e9d6b91c8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Node:
  def __init__(self, name, artists, parent):
    self.name = name
    self.artists = set(artists)
    self.parent = parent

  def __str__(self):
    out = self.name + " by "
    for a in self.artists:
      out += a + ", "
    out = out[:-2]
    return out

def get_tracks(artist: str, parent=None):
  output = []
  for i in range(0,750,50):
    result = sp.search(q='artist:' + artist, type='track', limit=50, offset=i)
    for entry in result['tracks']['items']:
      artists = []
      for a in entry['artists']:
        artists.append(a['name'])
      output.append(Node(entry['name'], artists, parent))
  return output

def songConnectHelper(current: str, explored, parent):
  output = set()
  #print("searching " + str(current))
  tracks = get_tracks(current, parent)
  for track in tracks:
    if (len(track.artists) > 1) and (any(current == a for a in track.artists)) and (track not in output):
      for a in track.artists:
        if a not in explored:
          output.add(track)
          break
  return output

def songConnect(start: str, end: str, max_depth = 4):
  explored = set()
  tree = [set() for _ in range(max_depth + 1)]
  tree[0] = {Node("DUMMY TRACK", [start], None)}
  for i in range(1, max_depth):
    for track in tree[i - 1]:
      for artist in track.artists:
        if artist not in explored:
          nodes = songConnectHelper(artist, explored, track)
          explored.add(artist)
          for t in nodes:
            for a in t.artists:
              if a != artist:
                tree[i].add(t)
    for t in tree[i]:
      for a in t.artists:
        if a == end:
          output = [str(t)]
          while t != None:
            t = t.parent
            output.append(str(t))
          output.reverse()
          return output[2:]
  return tree