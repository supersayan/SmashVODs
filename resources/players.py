from util import createLookupDict, lookup

pikaPlayerCorrections = {
  'ShinyMark': ['Shory\'s  ShinyMark'],
  'G-XTREME': ['G XTREME', 'XTREME', 'G-Extreme'],
  'Jiggs': ['Big Jiggs', 'Usain Jolt'],
  'H4': ['H4DS', 'BiB H4'],
  'Enki': ['IZI Enki'],
  'ESAM': ['PG ESAM'],
  'Abadango': ['あばだんご'],
  'Sho Limit': ['ショーリミ'],
  'Kishiru': ['キシル'],
  'ピロ': ['piro'],
  'Yuzha': ['Yuzuha'],
  'Hatsukami': ['ハツカミ/初雷', '初雷／ハツカミ', '初雷', 'ハツカミ']
}

pikaPlayerLookup = createLookupDict(pikaPlayerCorrections)

def correctPlayer(tag: str):
  return lookup(tag, pikaPlayerLookup)