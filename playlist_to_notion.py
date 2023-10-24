from integrations.youtube import pikaVodPlaylist
from integrations.notion import vodDb, notionAddVodToDb
from extract_data_from_title import extractDataFromTitle

'''
TODO:
fix player name regex for dittos/pika secondary
get pika vods by searching list of youtube channels instead of adding to playlist manually
fix regex not getting tags ending with v
'''

print('Getting Youtube Playlist...')
playlistItems = pikaVodPlaylist()

print('Getting VOD database...')
vodDbRows = vodDb()

print('Filtering videos already in db...')
playlistMap = {}
for vid in playlistItems:
  playlistMap[vid.contentDetails.videoId] = vid

vodDbMap = {}
for row in vodDbRows:
  vodDbMap[row['properties']['ID']['rich_text'][0]['plain_text']] = row

newVideos = [v for (k,v) in playlistMap.items() if k not in vodDbMap]

# Less Efficient
# newVideos: List[PlaylistItem] = list(filter(lambda video: 
#                     any((row['properties']['ID']['rich_text'][0]['plain_text'] == video.contentDetails.videoId) for row in vodDbRows),
#                   playlistItems))

print('Updating database...')
count = 0
for vid in newVideos:
  title = vid.snippet.title
  if (title == 'Deleted video' or title == 'Private video'):
    continue
  print(title)
  regexResults = extractDataFromTitle(title)
  notionAddVodToDb(vid, regexResults)
  count += 1

print(f'Added {count} new rows')
