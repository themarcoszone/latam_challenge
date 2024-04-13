from typing import List, Tuple
import orjson
from jsonpath_ng import parse
from collections import Counter
from memory_profiler import profile


log_f = open('q3_time.log', 'w')
@profile(stream=log_f)
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # JSONPATH where are the mentioned user in the tweet
    jsonpath_expr = parse('$[*].mentionedUsers[*].username')

    def read_json():
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return orjson.loads(f"[{','.join(lines)}]")

    items = read_json()

    return Counter([match.value for match in jsonpath_expr.find(items)]).most_common(10)

# path='../resources/farmers-protest-tweets-2021-2-4.json'
# q3_time(path)