from integrations.notion import vodDb

print('Getting VOD database...')
vodDbRows = vodDb()

print('Checking for duplicates...')
ids = set()
for row in vodDbRows:
  if row['properties']['ID']['rich_text'][0]['plain_text'] in ids:
    print(row['properties']['Title'])
  ids.add(row['properties']['ID']['rich_text'][0]['plain_text'])