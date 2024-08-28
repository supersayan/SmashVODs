from integrations.youtube import pikaVodPlaylist
from integrations.notion import vodDb, notionAddVodToDb
from extract_data_from_title import extractDataFromTitle

print('Getting Youtube Playlist...')
playlistItems = pikaVodPlaylist()

print('Getting Notion database...')
vodDbRows = vodDb()

print('Filtering videos not already in Notion...')
playlistMap = {}
for vid in playlistItems:
  playlistMap[vid.contentDetails.videoId] = vid

vodDbMap = {}
for row in vodDbRows:
  vodDbMap[row['properties']['ID']['rich_text'][0]['plain_text']] = row

newVideos = [v for (k,v) in playlistMap.items() if k not in vodDbMap]

print('Updating Notion database from Youtube playlist...')
count = 0
for vid in newVideos:
  title = vid.snippet.title
  if (title == 'Deleted video' or title == 'Private video'):
    continue
  print(f'** NEW: {title}')
  regexResults = extractDataFromTitle(title)
  notionAddVodToDb(vid, regexResults)
  count += 1

print(f'Added {count} new rows into Notion.')
