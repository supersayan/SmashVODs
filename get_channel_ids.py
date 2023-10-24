from integrations.youtube import pikaVodPlaylist
from pyyoutube import PlaylistItem

def getChannelIds():
    print('Getting Youtube Playlist...')
    playlistItems = pikaVodPlaylist()
    channels = {}

    vid: PlaylistItem
    for vid in playlistItems:
        if vid.snippet.videoOwnerChannelId is not None and vid.snippet.videoOwnerChannelId not in channels:
            channels[vid.snippet.videoOwnerChannelId] = vid.snippet.videoOwnerChannelTitle
    print(channels)
    return channels

getChannelIds()