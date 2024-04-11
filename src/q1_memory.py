from typing import List, Tuple
from datetime import datetime
import json
from collections import Counter

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
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    #Due to I need to minimize memory space, generator is a good approach
    def read_json():
        with open(file_path, 'r') as file:
            while line := file.readline():
                yield json.loads(line)

    items = read_json()
    date_user = []
    #get date and user for every item and append to a list
    for item in items:
        only_date = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S%z").date()
        date_user.append((only_date, item['user']['username']))

    #get the top 10 dates
    date_counts = Counter(date for date, _ in date_user).most_common(10)
    dates = [d for d, _ in date_counts]
    del date_counts
    result = []
    # for each top date get the top user. Append to the final result the date and user
    for d in dates:
        user_by_date = Counter(user for date, user in date_user if date == d).most_common(1)
        result.append((d, user_by_date[0][0]))

    return result

def q1_memory_v2(file_path: str) -> List[Tuple[datetime.date, str]]:
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
