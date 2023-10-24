from dotenv import load_dotenv
import os
from notion_client import Client as NotionClient

load_dotenv()
notion = NotionClient(auth=os.environ['NOTION_TOKEN'])

vodDatabaseId = '6843861011ef432090f3a16aee2086f5'
characterDatabaseId = '87d929c5c0154a34bbdd2b5f3507d844'

def notionGetDb(database_id: str, start_cursor: str = None):
  return notion.databases.query(database_id=database_id, start_cursor=start_cursor)

def notionGetDbFull(database_id: str):
  queryResponse = notionGetDb(database_id)
  rows = queryResponse.get('results')
  while (queryResponse.get('has_more')):
    queryResponse = notionGetDb(database_id, queryResponse.get('next_cursor'))
    rows += queryResponse.get('results')
  return rows

def vodDb():
  return notionGetDbFull(vodDatabaseId)

def notionGetCharacterDb() -> dict[str, str]:
  characterPageIds = {}
  for row in notionGetDbFull(characterDatabaseId):
    characterPageIds[row['properties']['Character']['title'][0]['text']['content']] = row['id']
  return characterPageIds

print('Getting Character database...')
characterPageIds = notionGetCharacterDb()

def notionAddVodToDb(video, regexResults):
  newPage = notion.pages.create(**{
    'parent': {
      'type': 'database_id',
      'database_id': vodDatabaseId,
    },
    'properties': {
      "Title": {
        "title": [{
          "text": {
            "content": video.snippet.title
          }
        }]
      },
      'Player': {
        'multi_select': list({'name': p} for p in regexResults.get('pikaPlayer')) if regexResults.get('pikaPlayer') else []
      },
      'VS Player': {
        'type': 'rich_text',
        'rich_text': [{
          'text': {'content': regexResults.get('otherPlayer')},
        }]
      },
      'Date': {
        'date': {
          'start': video.contentDetails.videoPublishedAt
        },
      },
      'ID': {
        'type': 'rich_text',
        'rich_text': [{
          'text': {'content': video.contentDetails.videoId},
        }]
      },
      'Matchups': {
        'relation': list(map(lambda c : { 'id': characterPageIds[c] }, regexResults['characters'])) if regexResults.get('characters') else []
      }
    },
    'cover': {
      'type': 'external',
      'external': {
        'url': video.snippet.thumbnails.maxres.url if video.snippet.thumbnails.maxres 
          else video.snippet.thumbnails.high.url if video.snippet.thumbnails.high
          else video.snippet.thumbnails.default.url,
      }
    }
  })
  notionAddVideo(newPage['id'], video.contentDetails.videoId)

def notionAddVideo(page_id: str, video_id: str):
  notion.blocks.children.append(**{
    'block_id': page_id,
    'children': [
      {
        'object': 'block',
        'type': 'video',
        'video': {
          'type': 'external',
          'external': {
            'url': f'https://www.youtube.com/watch?v={video_id}'
          }
        }
      }
    ]
  })

def notionGetPage(page_id):
  notion.pages.retrieve(**{
    'page_id': page_id
  })

def notionUpdateVodMatchups(page_id, characters: list[str]):
  notion.pages.update(**{
    'page_id': page_id,
    'properties': {
      'Matchups': {
        'relation': list(map(lambda c : { 'id': characterPageIds[c] }, characters))
      }
    }
  })