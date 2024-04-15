from typing import List, Tuple
import json
from jsonpath_ng import parse
from collections import Counter
# from memory_profiler import profile
#
#
# log_f = open('q3_memory.log', 'w')
# @profile(stream=log_f)
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # JSONPATH where are the mentioned user in the tweet
    jsonpath_expr = parse('mentionedUsers[*].username')

    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                # Given a json item, find all mentioned users in that tweet using this path $.mentionedUsers[*].username
                yield [match.value for match in jsonpath_expr.find(json.loads(line))]

    items = read_json()
    result = {}
    for item in items:
        # Sum previous result with new occurrences. Use augmented assignment |= operator to update/insert
        # new occurrences
        result |= {c: result.get(c, 0) + item.count(c) for c in item}

    return Counter(result).most_common(10)


# path = '../resources/farmers-protest-tweets-2021-2-4.json'
# q3_memory(path)