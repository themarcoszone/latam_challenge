from typing import List, Tuple
from datetime import datetime
import json
import pandas as pd


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    def read_dataframe():
        with open(file_path, 'r') as file:
            json_ob = json.loads(f"[{','.join(file.readlines())}]")
            return pd.DataFrame.from_dict(json_ob)

    df = read_dataframe()

    # Format columns to the needed types and values
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['username'] = df['user'].apply(lambda x: x['username'])

    # First count grouped by date, user
    date_user_counts = df.groupby(['date', 'username']).size().reset_index(name='count_by_user')

    # Now I want to add a column to get total y date. This will be helpful in next steps
    date_user_counts['tot_date'] = date_user_counts.groupby(['date'])['count_by_user'].transform('sum')

    # Get the user with max occurrence for a date. Then use nlargest to get the top 10 dates
    result_df = (date_user_counts.loc[date_user_counts.groupby('date')['count_by_user'].idxmax()]
                        [['date','username','count_by_user','tot_date']].nlargest(n=10, columns='tot_date', keep='all'))

    return list(result_df[['date', 'username']].to_records(index=False))
