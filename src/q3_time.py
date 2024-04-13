from typing import List, Tuple
import ujson
import json
from jsonpath_ng import parse
from collections import Counter


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # JSONPATH where are the mentioned user in the tweet
    jsonpath_expr = parse('$[*].mentionedUsers[*].username')

    def read_json():
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return ujson.loads(f"[{','.join(lines)}]")

    items = read_json()

    return Counter([match.value for match in jsonpath_expr.find(items)]).most_common(10)
