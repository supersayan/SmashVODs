from integrations.notion import vodDb, notionUpdateVodMatchups, notionUpdateVodPlayer
from resources.players import pikaPlayerCorrectionsInverse, correctPlayer

print('Getting VOD database...')
vodDbRows = vodDb()

print('Updating database...')
count = 0
for row in vodDbRows:
    # if not len(row['properties']['VS Character']['multi_select']):
        # characters = map(lambda c: c['name'], row['properties']['VS Character']['multi_select'])
        # notionUpdateVodMatchups(row['id'], characters)
    if len(row['properties']['Player']['multi_select']):
        correctPlayers = []
        for p in row['properties']['Player']['multi_select']:
            cp = correctPlayer(p['name'])
            if cp is not None and cp != p['name']:
                correctPlayers.append(cp)
        if len(correctPlayers):
            print(row['properties']['Title']['title'][0]['text']['content'])
            notionUpdateVodPlayer(row['id'], map(lambda p: correctPlayer(p['name']) or p['name'], row['properties']['Player']['multi_select']))
            count += 1

print(f'Updated {count} rows')