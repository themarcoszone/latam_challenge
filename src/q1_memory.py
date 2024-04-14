from typing import List, Tuple
from datetime import datetime
import json
from collections import Counter
from memory_profiler import profile



'''
Approach 1:
- Get a list with all tuples (date, username)
- Get top 10 of posted dates
- Get top 1 user who posted in each day

Approach 2
- Get top 10 of dates
- After that filter users who posted in those days
- For each day get the top user who posted that day   
'''
log_f = open('q1_memory.log', 'w')
@profile(stream=log_f)
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                yield json.loads(line)

    items = read_json()
    count_dates = {}
    # get date for every item and append to a list
    for item in items:
        only_date = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S%z").date()
        count_dates[only_date] = count_dates.get(only_date, 0) + 1

    #get the top 10 dates
    dates_top_10 = Counter(count_dates).most_common(10)
    del count_dates
    dates = [d for (d, _) in dates_top_10]
    del dates_top_10
    result = []
    #now get the top user by each top date. Once the top user is get insert in final result the (date, user)
    for d in dates:
        user_gen = read_json()
        user_by_d = {}
        for u in user_gen:
            if datetime.strptime(u['date'], "%Y-%m-%dT%H:%M:%S%z").date() == d:
                user_by_d[u['user']['username']] = user_by_d.get(u['user']['username'], 0) + 1

        result.append((d, Counter(user_by_d).most_common(1)[0][0]))
        del user_by_d

    return result



