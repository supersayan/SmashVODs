from util import createLookupDict, lookup

characterCorrections: dict[str, list[str]] = {
  'Mario': ['マリオ'],
  'Donkey Kong': ['DK', 'ドンキーコング'],
  'Link': ['リンク'],
  'Samus / Dark Samus': ['Samus', 'Dark Samus', 'サムス', 'ダークサムス'],
  'Yoshi': ['ヨッシー'],
  'Kirby': ['カービィ'],
  'Fox': ['フォックス'],
  'Pikachu': ['Pika', 'ピカチュウ'],
  'Luigi': ['ルイージ'],
  'Ness': ['ネス'],
  'Captain Falcon': ['Cpt Falcon', 'C. Falcon', 'Falcon', 'キャプテン・ファルコン'],
  'Jigglypuff': ['Puff', 'プリン'],
  'Peach / Daisy': ['Peach', 'Daisy', 'Paisy', 'ピーチ', 'デイジー'],
  'Bowser': ['クッパ'],
  'Ice Climbers': ['アイスクライマー'],
  'Sheik': ['Shiek', 'シーク'],
  'Zelda': ['ゼルダ'],
  'Dr. Mario': ['Dr Mario', 'ドクターマリオ'],
  'Pichu': ['ピチュー'],
  'Falco': ['ファルコ'],
  'Marth': ['マルス'],
  'Lucina': ['ルキナ'],
  'Young Link': ['YL', 'YLink', 'こどもリンク'],
  'Ganondorf': ['Ganon', 'ガノンドロフ'],
  'Mewtwo': ['ミュウツー'],
  'Roy': ['ロイ'],
  'Chrom': ['クロム'],
  'Mr. Game & Watch': ['Game & Watch', 'Game and Watch', 'Mr Game & Watch', 'Mr Game and Watch', 
                       'G&W', 'Mr.ゲーム＆ウォッチ', 'ゲーム＆ウオッチ'],
  'Meta Knight': ['メタナイト'],
  'Pit / Dark Pit': ['Pit', 'Dark Pit', 'ピット', 'ブラックピット'],
  'Zero Suit Samus': ['ZSS', 'ゼロスーツサムス'],
  'Wario': ['ワリオ'],
  'Snake': ['スネーク'],
  'Ike': ['アイク'],
  'Pokémon Trainer': ['PT', 'Pokemon Trainer', 'ポケモントレーナー'],
  'Diddy Kong': ['Diddy', 'ディディーコング'],
  'Lucas': ['リュカ'],
  'Sonic': ['ソニック'],
  'King Dedede': ['Dedede', 'デデデ'],
  'Olimar': ['Alph', 'ピクミン&オリマー'],
  'Lucario': ['ルカリオ'],
  'R.O.B.': ['ROB', 'R.O.B', 'ロボット'],
  'Toon Link': ['TLink', 'トゥーンリンク'],
  'Wolf': ['ウルフ'],
  'Villager': ['むらびと'],
  'Mega Man': ['Mega-man', 'ロックマン'],
  'Wii Fit Trainer': ['WFT', 'Wii Fit', 'Wii Fitトレーナー'],
  'Rosalina & Luma': ['Rosa', 'Rosalina', 'ロゼッタ&チコ', 'ロゼッタ＆チコ'],
  'Little Mac': ['リトル・マック'],
  'Greninja': ['ゲッコウガ', 'Amphinobi'],
  'Mii Brawler': ['Mii 格闘タイプ', '格闘Mii', 'Mii格闘', 'Mii Boxeur'],
  'Mii Swordfighter': ['Mii 剣術タイプ', '剣術Mii', 'Mii剣術'],
  'Mii Gunner': ['Mii 射撃タイプ', '射撃Mii', 'Mii射撃'],
  'Palutena': ['パルテナ'],
  'Pac-Man': ['Pac man', 'パックマン'],
  'Robin': ['ルフレ', 'Daraen'],
  'Shulk': ['シュルク'],
  'Bowser Jr.': ['Bowser Jr', 'Koopaling', 'Larry', 'Wendy', 'Iggy', 'Morton', 'Lemmy', 'Ludwig', 'クッパJr.'],
  'Duck Hunt': ['Duck Hunt Duo', 'DH', 'ダックハント'],
  'Ryu': ['リュウ'],
  'Ken': ['ケン'],
  'Cloud': ['クラウド'],
  'Corrin': ['カムイ'],
  'Bayonetta': ['Bayo', 'ベヨネッタ'],
  'Inkling': ['インクリング'],
  'Ridley': ['リドリー'],
  'Simon / Richter': ['Simon', 'Richter', 'Belmont', 'シモン', 'リヒター'],
  'King K. Rool': ['K Rool', 'King K Rool', 'キングクルール'],
  'Isabelle': ['しずえ'],
  'Incineroar': ['Incin', 'ガオガエン'],
  'Piranha Plant': ['Plant', 'パックンフラワー'],
  'Joker': ['ジョーカー'],
  'Hero': ['勇者'],
  'Banjo & Kazooie': ['Banjo', 'Banjo and Kazooie', 'バンジョー&カズーイ', 'バンジョー＆カズーイ', 'バンジョー'],
  'Terry': ['テリー'],
  'Byleth': ['ベレト', 'ベレス'],
  'Min Min': ['ミェンミェン'],
  'Steve': ['Steve & Alex', 'Alex', 'Zombie', 'Enderman', 'スティーブ', 'アレックス', 'ゾンビ', 'エンダーマン'],
  'Sephiroth': ['セフィロス'],
  'Pyra & Mythra': ['Aegis', 'Pyra', 'Mythra', 'Pyra Mythra', 'Pyra and Mythra', 'ホムラ', 'ヒカリ'],
  'Kazuya': ['カズヤ'],
  'Sora': ['ソラ'],
}

characterCorrectionsInverse = createLookupDict(characterCorrections)

def correctCharacter(name: str):
  res = lookup(name, characterCorrectionsInverse)
  if res:
    return res
  elif name in characterCorrections:
    return name
  else:
    return None