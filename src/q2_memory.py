from typing import List, Tuple
import json
import emoji
import regex
from collections import Counter
from memory_profiler import profile


log_f = open('q2_memory.log', 'w')
@profile(stream=log_f)
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                # I assume that post text content is in field content or renderedContent. So, I've decided to use
                # renderedContent
                yield json.loads(line)['renderedContent']

    items = read_json()
    result = {}
    for item in items:
        # Using regex module allows to find grapheme clusters ocurrences.
        # Source: https://www.w3.org/International/questions/qa-indic-graphemes#patronymic
        # item contains the post, so I need to iterate through each character to determine if is an emoji
        words = regex.findall(r'\X', item)
        # Sum previous result with new occurrences. Use augmented assignment |= operator to update/insert
        # new occurrences
        result |= {c: result.get(c, 0) + words.count(c) for c in words if emoji.is_emoji(c)}

    return Counter(result).most_common(10)
