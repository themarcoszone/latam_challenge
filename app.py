from src.q1_memory import q1_memory
from src.q2_memory import q2_memory
from src.q3_memory import q3_memory

from cProfile import Profile
from pstats import Stats, SortKey
from src.q1_time import q1_time
from src.q2_time import q2_time
from src.q3_time import q3_time

file_path = "resources/test.json"
# Check memory profile
print(q1_memory(file_path))
print(q2_memory(file_path))
print(q3_memory(file_path))

# Check time performance
print('Checking time for q1_time')
with Profile() as profile:
    print(q1_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )

print('Checking time for q2_time')
with Profile() as profile:
    print(q2_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )

print('Checking time for q3_time')
with Profile() as profile:
    print(q3_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )
