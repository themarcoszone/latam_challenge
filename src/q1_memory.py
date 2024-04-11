import sys
from typing import List, Tuple
from datetime import datetime
import json
from collections import Counter
from memory_profiler import profile, memory_usage

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
log_mem = open('memory.log', 'w+')
@profile(stream=log_mem)
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    #Due to I need to minimize memory space, generator is a good approach
    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                yield json.loads(line)

    items = read_json()
    date_user = []
    for item in items:
        only_date = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S%z").date()
        date_user.append((only_date, item['user']['username']))

    date_counts = Counter(date for date, _ in date_user).most_common(10)
    dates = [d for d, _ in date_counts]
    del date_counts
    result = []
    for d in dates:
        user_by_date = Counter(user for date, user in date_user if date == d).most_common(1)
        result.append((d, user_by_date[0][0]))

    #count_dates = sorted(count_dates.items(), key=lambda x: x[1], reverse=True)
    return result

@profile(stream=log_mem)
def q1_memory_v2(file_path: str) -> List[Tuple[datetime.date, str]]:
    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                yield json.loads(line)

    items = read_json()
    count_dates = {}

    for item in items:
        only_date = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S%z").date()
        count_dates[only_date] = count_dates.get(only_date, 0) + 1

    dates_top_10 = Counter(count_dates).most_common(10)
    del count_dates
    #dates_top_10 = sorted(count_dates.items(), key=lambda x: x[1], reverse=True)[:10]
    dates = [d for (d, _) in dates_top_10]
    del dates_top_10
    result = []
    for d in dates:
        user_gen = read_json()
        user_by_d = {}
        for u in user_gen:
            if datetime.strptime(u['date'], "%Y-%m-%dT%H:%M:%S%z").date() == d:
                user_by_d[u['user']['username']] = user_by_d.get(u['user']['username'], 0) + 1

        result.append((d, Counter(user_by_d).most_common(1)[0][0]))
        del user_by_d

    return result

# json_path = '../resources/farmers-protest-tweets-2021-2-4.json'
# #json_path = '../resources/test.json'
# # q1_memory(json_path)
# # q1_memory_v2(json_path)
# # mem_usage_1 = memory_usage((q1_memory, (), {'file_path': '../resources/farmers-protest-tweets-2021-2-4.json'}), max_usage=True)
# # mem_usage_2 = memory_usage((q1_memory_v2, (), {'file_path': '../resources/farmers-protest-tweets-2021-2-4.json'}), max_usage=True)
# # print(mem_usage_1)
# # print(mem_usage_2)