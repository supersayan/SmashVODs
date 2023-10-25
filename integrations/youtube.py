from dotenv import load_dotenv
import os
from pyyoutube import Client
import webbrowser

load_dotenv()
youtube = Client(api_key=os.environ['YOUTUBE_API_KEY'])

youtubeOAuth = None

def instantiateOAuthClient():
  cli = Client(client_id=os.environ['YOUTUBE_CLIENT_ID'], client_secret=os.environ['YOUTUBE_CLIENT_SECRET'])
  if os.environ['YOUTUBE_REFRESH_TOKEN']:
    cli.refresh_access_token(os.environ['YOUTUBE_REFRESH_TOKEN'])
  else:
    authUrl = cli.get_authorize_url()
    print(authUrl)
    webbrowser.open(authUrl[0])
    authResponse = input('Enter redirected url: ')
    cli.generate_access_token(authorization_response=authResponse)
    os.environ['YOUTUBE_REFRESH_TOKEN'] = cli.refresh_token
  global youtubeOAuth
  youtubeOAuth = cli

pikaVodPlaylistId = 'PLc-VgMHSQbqkcN-jPP2GqLUcH7MR-_DJm'

# Get list of videos from yt playlist
def youtubePlaylistList(playlistId: str, pageToken: str = None):
  return youtube.playlistItems.list(playlist_id=playlistId, parts='contentDetails,id,snippet', max_results=50, page_token=pageToken)

def youtubePlaylistListAll(playlistId: str, pageLimit: int = 0):
  playlistResponse = youtubePlaylistList(playlistId)
  playlistItems = playlistResponse.items
  nextPageToken = playlistResponse.nextPageToken

  count = pageLimit - 1
  while (nextPageToken and count != 0):
    playlistResponse = youtubePlaylistList(playlistId, nextPageToken)
    playlistItems += playlistResponse.items
    nextPageToken = playlistResponse.nextPageToken
    count -= 1

  pages = (count - pageLimit) * -1

  return playlistItems

def pikaVodPlaylist():
  return youtubePlaylistListAll(pikaVodPlaylistId)

def addToPlaylist(videoId, playlistId = pikaVodPlaylistId):
  if not youtubeOAuth:
    instantiateOAuthClient()
  return youtubeOAuth.playlistItems.insert(parts='snippet', body={
    'snippet': {
      'playlistId': playlistId,
      'resourceId': {
        'kind': 'youtube#video',
        'videoId': videoId,
      }
    }
  })