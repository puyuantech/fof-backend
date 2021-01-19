import numpy as np
import pandas as pd
from .raw_data_helper import RawDataHelper
from ...view.raw_models import OSFundInfo, OSFundNav, OSFundBenchmark, OSStockInfo, OSCorpBondInfo, OSGovtBondInfo, OSComdtyInfo, OSIndexFutureInfo, OSMtgeBondInfo, EmOverseaStockFinFac

# df.to_sql('em_oversea_stock_fin_fac', RawDatabaseConnector().get_engine(), index=False, if_exists='append')

class OtherRawDataDownloader:

    def __init__(self, data_helper):
        self._data_helper = data_helper

    def oversea_fund_info(self, fund_info):
        fund_info_dic = {
            '基金id':'codes',
            '基金名称':'desc_name',
            '基金管理公司':'company_name',
            '基金类型':'fund_type',
            '行业':'industry',
            '地区':'area',
            '最新净值':'latest_nav',
            '基金系列':'fund_series',
            '是否为新基金':'is_new_fund',
            '赎回资金到账天数':'redeem_dates',
            '换出基金指示滞延时间':'excg_out_t_delay',
            '换入基金指示滞延时间':'excg_in_t_delay',
            '最低初始投资额':'min_init_trade_amt',
            '最低后续投资额':'min_ag_trade_amt',
            '最小赎回类型':'min_redeem_type',
            '最小赎回数量':'min_redeem_vol',
            '最小持有类型':'min_pos_type',
            '最小持有数量':'min_pos_vol',
            '申购周期':'purchase_period',
            '风险级别':'risk_level',
            '可供认购':'is_purchase',
            '证监会是否认可':'is_CSRC_approve',
            '年费':'yearly_fee',
            '申购处理频率':'purchase_process_freq',
            '币种':'money_type',
            '支持转换基金':'is_sup_exchg_fund',
            '支持转换为同系列其他基金':'is_sup_same_series_fund',
            '支持同系列其他基金转换为本基金':'is_sup_same_series_exchg',
            '赎回费(%)':'redeem_fee',
            '赎回方式':'redeem_method',
            '是否衍生产品':'is_derivatives',
            '股息分派方式':'divident_distbt_mtd',
            '派息频率':'divident_freq',
            '资产类别':'asset_type',
            '资产编号':'asset_code',
            '发行日期':'issue_date',
            '发行价':'issue_price',
            '基金规模（单位：百万）':'fund_size_biln',
            '基金规模统计日期':'fund_size_calc_date',
            '基金规模币种':'fund_size_money_type',
            '费率':'fee_rate',
            '费率统计日期':'fee_calc_date',
            '复杂产品':'is_compx_product',
        }
        delete_cols = ['发布日期','处理结果']
        date_list = ['发行日期','费率统计日期','基金规模统计日期']
        con_list = ['是否为新基金','可供认购','证监会是否认可','支持转换基金','支持转换为同系列其他基金',
                '是否衍生产品','复杂产品','支持同系列其他基金转换为本基金']

        for date_col in date_list:
            td = pd.to_datetime(fund_info[date_col])
            td = [i.date() for i in td]
            fund_info.loc[:,date_col] = td

        for del_col in delete_cols:
            fund_info = fund_info.drop(columns=[del_col])

        for con_col in con_list:
            fund_info.loc[:,con_col] = fund_info[con_col].replace({'是':True, '否':False,})
            
        fund_info = fund_info.rename(columns=fund_info_dic)
        self._data_helper._upload_raw(fund_info, OSFundInfo.__table__.name)

    def oversea_fund_nav(self, df):
        td = pd.to_datetime(df.datetime)
        td = [i.date() for i in td]
        df['datetime'] = td
        self._data_helper._upload_raw(df, OSFundNav.__table__.name)

    def oversea_fund_benchmark(self, df):
        dic = {
            '#N/A Field Not Applicable':None,
            '#N/A Invalid Security':None,
        }
        df = df.replace(dic)
        self._data_helper._upload_raw(df, OSFundBenchmark.__table__.name)

    def oversea_stock_info(self, df):
        df = df.rename(columns={'code':'codes','stock name':'stock_name_e','证券简称':'stock_name_c','行业分类':'industry'}).drop(columns=['number'])
        df.loc[:,'district_code'] = df.codes.map(lambda x: x.split(' ')[1])
        self._data_helper._upload_raw(df, OSStockInfo.__table__.name)

    def oversea_corp_bond_info(self, df):
        df = df.rename(columns={'code':'codes','债券名称/公司名称':'bond_name_e','公司名称-繁体中文':'company_name_c','债券对应的股票代码':'company_code','国家全称':'district_name_e','行业分类-一级':'industry_1','行业分类-二级':'industry_2','行业分类-三级':'industry_3','到期日':'maturity','穆迪评级':'md_rate','标普评级':'sp_rate','惠誉评级':'hy_rate','ISIN':'isin_code'}).drop(columns=['number'])
        df = df.replace('#N/A Field Not Applicable',None)
        td = pd.to_datetime(df.maturity)
        df.maturity = [i.date() for i in td]
        self._data_helper._upload_raw(df, OSCorpBondInfo.__table__.name)
        
    def oversea_govt_bond_info(self, df):
        df = df.rename(columns={'code':'codes','债券名称/公司名称':'bond_name_e','公司名称-繁体中文':'bond_name_c','国家全称':'district_name','到期日':'maturity','穆迪评级':'md_rate','标普评级':'sp_rate','惠誉评级':'hy_rate','ISIN':'isin_code','发行金额':'total_amount'}).drop(columns=['number'])
        df = df.replace('#N/A Field Not Applicable',None)
        td = pd.to_datetime(df.maturity)
        df.maturity = [i.date() for i in td]
        self._data_helper._upload_raw(df, OSGovtBondInfo.__table__.name)

    def oversea_comdty_info(self, df):
        df = df.rename(columns={'code':'codes','证券名称':'asset_name_e','证券类型':'future_type','期货合约到期日':'maturity'}).drop(columns=['number'])
        df = df.replace('#N/A Field Not Applicable',None)
        td = pd.to_datetime(df.maturity)
        df.maturity = [i.date() for i in td]
        self._data_helper._upload_raw(df, OSComdtyInfo.__table__.name)
        return df

    def oversea_index_info(self, df):
        df = df.rename(columns={'code':'codes','证券名称':'asset_name_c','期货合约到期日':'maturity'}).drop(columns=['number'])
        df = df.replace('#N/A Field Not Applicable',None)
        td = pd.to_datetime(df.maturity)
        df.maturity = [i.date() for i in td]
        df.loc[:,'asset_type'] = 'Index'
        self._data_helper._upload_raw(df, OSIndexFutureInfo.__table__.name)

    def oversea_mtge_bond_info(self, df):
        df = df.rename(columns={'code':'codes','资产类别':'asset_type','证券名称':'bond_name_e','抵押债本金偿付期限开始日期':'mtge_pay_start','抵押债本金偿付期限结束日期':'mtge_pay_end','ISIN':'isin_code'}).drop(columns='number')
        td = pd.to_datetime(df.mtge_pay_start)
        df.mtge_pay_start = [i.date() for i in td]
        td = pd.to_datetime(df.mtge_pay_end)
        df.mtge_pay_end = [i.date() for i in td]
        self._data_helper._upload_raw(df, OSMtgeBondInfo.__table__.name)

    def oversea_stock_fin_fac(self, df):
        f = '/Users/huangkejia/Home/'
        market=['全部美股','全部港股']
        stock_list = ['_19_4.xls','_20_1.xls','_20_2.xls','_20_3.xls']
        date_dic = {
            '_19_4.xls':'20191231',
            '_20_1.xls':'20200331',
            '_20_2.xls':'20200630',
            '_20_3.xls':'20200930',
        }
        res = []
        res_cols = []
        for market_i in market:
            for stock_i in stock_list:
                df = pd.read_excel(f+market_i+stock_i).dropna(subset=['证券名称'])
                df.columns = [i.split('\r\n')[0] for i in df.columns]
                df = df.drop(columns=['市盈率(PE)','市净率(PB)','市销率(PS)','股息率'], errors='ignore')
                df.loc[:,'report_date'] = date_dic[stock_i]
                df = df.loc[:,~df.columns.duplicated()]
                cols = df.columns.tolist()
                df = df[sorted(cols)]
                res_cols.append(cols)
                res.append(df)

        df = pd.concat(res)
        dic = {
            'report_date':'report_date',
            '已发行普通股':'indicator_1',
            '年度分红':'indicator_2',
            '归属母公司净利润(TTM)':'indicator_3',
            '每股净资产':'indicator_4',
            '每股净资产(最新股本摊薄)':'indicator_5',
            '每股收益EPS(基本)':'indicator_6',
            '每股收益EPS(稀释)':'indicator_7',
            '每股收益EPS(调整股本数)':'indicator_8',
            '每股派息':'indicator_9',
            '每股现金流量净额':'indicator_10',
            '每股现金流量净额(TTM)':'indicator_11',
            '每股经营现金净流量':'indicator_12',
            '每股经营现金净流量(TTM)':'indicator_13',
            '每股营业收入':'indicator_14',
            '稀释每股收益':'indicator_15',
            '经营活动产生的现金':'indicator_16',
            '营业收入':'indicator_17',
            '证券代码':'stock_code',
            '证券名称':'desc_name',
        }
        df = df.rename(columns=dic)
        '''
        for i,j in dic.items():
            if j in ['report_date','stock_code','desc_name']:
                data_row = f'{j} = Column(CHAR(20)) # {i} '
            else:
                data_row = f'{j} = Column(DOUBLE(asdecimal=False)) # {i} '
            print(data_row)
        '''
        df= df.replace('——',np.nan)
        self._data_helper._upload_raw(df, EmOverseaStockFinFac.__table__.name)