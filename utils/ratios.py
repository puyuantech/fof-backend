import empyrical as ep
import pandas as pd
import numpy as np


def draw_down_underwater(nav):
    """
    回撤水下
    :param nav:
    :return:
    """
    running_max = np.maximum.accumulate(nav)
    return -100 * ((running_max - nav) / running_max)


def monthly_return(returns):
    """
    月度收益
    :param returns:
    :return:
    """
    ret = ep.aggregate_returns(returns, 'monthly')
    ret = pd.DataFrame(ret)
    ret.index = ['{}-{}'.format(index[0], index[1]) for index in ret.index]
    return {
        'ret': ret['ret'].to_list(),
        'index': ret.index,
    }


def yearly_return(returns):
    """
    年度收益
    :param returns:
    :return:
    """
    ret = ep.aggregate_returns(returns, 'yearly')
    ret = pd.DataFrame(ret)
    ret = ret.reset_index()
    return ret.to_dict(orient='list')


if __name__ == '__main__':
    print(draw_down_underwater(np.array([1, 1.2, 1.3, 1, 1.6, 2])))




