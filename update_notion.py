from integrations.notion import vodDb, notionUpdateVodMatchups

print('Getting VOD database...')
vodDbRows = vodDb()

print('Updating database...')
count = 0
for row in vodDbRows:
    if not len(row['properties']['Matchups']['relation']):
        characters = map(lambda c: c['name'], row['properties']['VS Character']['multi_select'])
        notionUpdateVodMatchups(row['id'], characters)
        count += 1

print(f'Updated {count} rows')