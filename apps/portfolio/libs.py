
from pandas import DataFrame

from utils.helper import replace_nan


def get_title_and_items(df: DataFrame):
    df = df.reset_index().to_dict('list')
    return {
        'title': df.pop('index_id'),
        'items': [{'key': k, 'value': replace_nan(v)} for k, v in df.items()],
    }

