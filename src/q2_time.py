from typing import List, Tuple
import pandas as pd
import emoji
import regex


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    import json
    from collections import Counter
    def read_json():
        with open(file_path, 'r') as file:
            return json.loads(f"[{','.join(file.readlines())}]")

    items = read_json()
    result = {}
    for item in items:
        # Using regex module allows to find grapheme clusters ocurrences.
        # Source: https://www.w3.org/International/questions/qa-indic-graphemes#patronymic
        # item contains the post, so I need to iterate through each character to determine if is an emoji
        words = regex.findall(r'\X', item['renderedContent'])
        # Sum previous result with new occurrences. Use augmented assignment |= operator to update/insert
        # new occurrences
        result |= {c: result.get(c, 0) + words.count(c) for c in words if emoji.is_emoji(c)}

    return Counter(result).most_common(10)

#Subotpimal solution
def q2_time_v2(file_path: str) -> List[Tuple[str, int]]:
    df = pd.read_json(file_path, lines=True)
    # Get a list of emojis in a given text
    df['emojis'] = df['renderedContent'].apply(
                                lambda x: [c for c in regex.findall(r'\X', x) if emoji.is_emoji(c)])

    #df = df.loc[:, ~df.columns.isin(['emojis'])]
    # I need to explode that emoji list
    exploded_df = df.explode('emojis')
    # Count emojis occurrence
    exploded_df = exploded_df.groupby('emojis').size().reset_index(name='count_emojis')
    # Keep the top 10 used emojis
    exploded_df = exploded_df.nlargest(n=10, columns='count_emojis', keep='all')

    return list(exploded_df[['emojis', 'count_emojis']].to_records(index=False))
