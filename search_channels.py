from integrations.youtube import pikaVodPlaylist, youtubePlaylistListAll, addToPlaylist
from integrations.notion import notionAddVodToDb
from extract_data_from_title import extractDataFromTitle

from pyyoutube import PlaylistItem
from datetime import datetime, timedelta, timezone
import re
import webbrowser

print('Getting Youtube Playlist...')
pikaVods = pikaVodPlaylist()

channels: dict[str, str] = {}
vid: PlaylistItem
for vid in pikaVods:
    if vid.snippet.videoOwnerChannelId is not None and vid.snippet.videoOwnerChannelId not in channels:
        channels[vid.snippet.videoOwnerChannelId] = vid.snippet.videoOwnerChannelTitle

pikaPlaylistSet = set()
for vid in pikaVods:
  pikaPlaylistSet.add(vid.contentDetails.videoId)

pikaRegex = r"[\(（](?:Pikachu|ピカチュウ)[\)|）]"
channelCount = 0
count = 0
for channelId, channelName in channels.items():
    print(channelName)
    channelVids = youtubePlaylistListAll('UU' + channelId[2:], 2)
    for vid in channelVids:
        publishedAt = datetime.fromisoformat(vid.contentDetails.videoPublishedAt[:10])
        if (datetime.now() - publishedAt) > timedelta(days=365):
            continue
        title = vid.snippet.title
        if (re.search(pikaRegex, title) is None):
            continue
        if (re.search('Melee|SSBM|SSB4|Sm4sh|Smash 4|Reverse Mains', title) is not None):
            continue
        if (vid.contentDetails.videoId not in pikaPlaylistSet):
            print(vid.snippet.title)
            addToPlaylist(vid.contentDetails.videoId)
            regexResults = extractDataFromTitle(title)
            notionAddVodToDb(vid, regexResults)
            count += 1
    channelCount += 1
    if channelCount >= 30:
        break

print(f'Added {count} new videos')