import threading
from dotenv import load_dotenv, set_key
import os
from pyyoutube import Client
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import logging

load_dotenv()
youtube = Client(api_key=os.environ['YOUTUBE_API_KEY'])
youtubeOAuth = None

REDIRECT_URI_PORT = 2274

def instantiateOAuthClient():
  load_dotenv()
  cli = Client(client_id=os.environ['YOUTUBE_CLIENT_ID'], client_secret=os.environ['YOUTUBE_CLIENT_SECRET'])
  if 'YOUTUBE_REFRESH_TOKEN' in os.environ:
    cli.refresh_access_token(os.environ['YOUTUBE_REFRESH_TOKEN'])
    if (cli.access_token is not None):
      return

  authUrl = cli.get_authorize_url(redirect_uri=f'https://localhost:{REDIRECT_URI_PORT}/')

  global youtubeOAuth
  youtubeOAuth = cli

  httpd = HTTPServer(('localhost', REDIRECT_URI_PORT), ServerHandler)
  context = get_ssl_context("cert.pem", "key.pem")
  httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
  logging.info(f'authorization URL: {authUrl[0]}')
  webbrowser.open(authUrl[0])
  httpd.serve_forever()

  # while (youtubeOAuth.access_token is None):
  #   time.sleep(5)
  # time.sleep(30)
  # print(youtubeOAuth.access_token)
  # httpd.server_close()
  # set_key(dotenv_path='integrations/.env', key_to_set='YOUTUBE_REFRESH_TOKEN', value_to_set=cli.refresh_token)

class ServerHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    try:
      authResponse = f'https://localhost:{REDIRECT_URI_PORT}{self.path}'
      youtubeOAuth.generate_access_token(authorization_response=authResponse, redirect_uri=f'https://localhost:{REDIRECT_URI_PORT}/')
      set_key(dotenv_path='integrations/.env', key_to_set='YOUTUBE_REFRESH_TOKEN', value_to_set=youtubeOAuth.refresh_token)
      self.send_response(200)
      self.end_headers()
    finally:
      t = threading.Thread(target = self.server.shutdown)
      t.daemon = True
      t.start()

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

  return playlistItems

def pikaVodPlaylist():
  return youtubePlaylistListAll(pikaVodPlaylistId)

def addToPlaylist(videoId, playlistId = pikaVodPlaylistId):
  if not youtubeOAuth:
    instantiateOAuthClient()
    if youtubeOAuth is not None:
      logging.info('Youtube OAuth success')
    else:
      logging.error('Youtube OAuth failed')
  logging.debug('Inserting item to playlist...')
  return youtubeOAuth.playlistItems.insert(parts='snippet', body={
    'snippet': {
      'playlistId': playlistId,
      'resourceId': {
        'kind': 'youtube#video',
        'videoId': videoId,
      }
    }
  })

def get_ssl_context(certfile, keyfile):
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  context.load_cert_chain(os.path.join(os.path.dirname(__file__), certfile), os.path.join(os.path.dirname(__file__), keyfile))
  context.set_ciphers("@SECLEVEL=1:ALL")
  return context
# Command used to create cert and key files:
# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem