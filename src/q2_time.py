from typing import List, Tuple
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

