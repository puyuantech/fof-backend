import pandas as pd

from surfing.data.api.basic import BasicDataApi


class SurfingQuery:

    @staticmethod
    def get_index_point(index_id, start_date='', end_date='', columns=('close',)):
        df = BasicDataApi().get_index_price_dt(
            start_date=start_date,
            end_date=end_date,
            index_list=(index_id,),
            columns=columns,
        )
        df = df.sort_values('datetime')

        if len(df) < 1:
            columns = ['datetime', index_id] + list(columns)
            return pd.DataFrame([], columns=columns)

        return df
