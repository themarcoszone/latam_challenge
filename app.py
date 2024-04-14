from cProfile import Profile
from pstats import Stats, SortKey
import logging


from src.q1_memory import q1_memory
from src.q2_memory import q2_memory
from src.q3_memory import q3_memory

from src.q1_time import q1_time
from src.q2_time import q2_time
from src.q3_time import q3_time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

file_path = "farmers-protest-tweets-2021-2-4.json"
# Check memory profile
logger.info(q1_memory(file_path))
logger.info(q2_memory(file_path))
logger.info(q3_memory(file_path))

# Check time performance
logger.info('Checking time for q1_time')
with Profile() as profile:
    logger.info(q1_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )

logger.info('Checking time for q2_time')
with Profile() as profile:
    logger.info(q2_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )

logger.info('Checking time for q3_time')
with Profile() as profile:
    logger.info(q3_time(file_path))
    (
     Stats(profile)
     .strip_dirs()
     .sort_stats(SortKey.TIME)
     .print_stats(15)
    )
