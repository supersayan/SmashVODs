def createLookupDict(dict: dict[str, list[str]]) -> dict[str, str]:
  inverse = {}
  for k,v in dict.items():
    for x in v:
      inverse[normalize(x)] = k
    kNormalized = normalize(k)
    if kNormalized not in inverse:
      inverse[kNormalized] = k
  return inverse

def lookup(string: str, lookupDict: dict[str, str]):
  return lookupDict.get(normalize(string))

def normalize(string: str):
  return ''.join(string.lower().split())