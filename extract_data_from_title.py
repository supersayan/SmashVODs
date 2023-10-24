from resources.characters import correctCharacter
from resources.players import correctPlayer
import re

'''
Notion database item format: 
Title: title
ID: rich_text
Date: date
Player: rich_text
VS Character: multi_select
VS Player: rich_text
Characters: relation
'''

# Use regex to get Player tags and Smash Characters
startingDelim = "-\s|vs?\.?\s|\||—|–|:|\]|＞|戦|\/|SP"

playerRegex = f"(?:^|(?:{startingDelim})\s*)((?:(?!{startingDelim}).)*?\S)\s?[\(（](.*?)[\)|）]"

def extractDataFromTitle(title: str):
  regexResults = {
    'characters': set(),
    'pikaPlayer': set(),
    'otherPlayer': '',
  }

  matches = re.findall(playerRegex, title, flags=re.I)
  # Returns list of tuples [ (Player 1, Player 1 characters), (Player 2, Player 2 characters) ]
  for match in matches:
    characters = set()
    for char in re.split('[,\/、]', match[1]):
      corrected = correctCharacter(char)
      if corrected:
        characters.add(corrected)

    if ('Pikachu' in characters):
      regexResults['pikaPlayer'].add(match[0])
    elif len(characters) > 0:
      regexResults['characters'] = characters
      regexResults['otherPlayer'] = match[0]

  return regexResults