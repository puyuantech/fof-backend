import pandas as pd
import io
import datetime
import traceback
from flask import make_response, request, g
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.globals import db
from models import FOFNav, FOFInfo
from utils.decorators import login_required
from utils.helper import replace_nan
from surfing.util.calculator import Calculator
from surfing.data.manager.manager_hedge_fund import HedgeFundDataManager


class NavTemplateFile(ApiViewHandler):

    def get(self):
        df = pd.DataFrame(data=[], columns=['日期', '单位净值', '累计净值'])

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        df.to_excel(excel_writer=writer, index=False, sheet_name='sheet0')
        writer.save()
        file_name = 'template.xlsx'
        response = make_response(out.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        response.headers["Content-type"] = "application/x-xls"
        writer.close()
        return response


class NavParseFile(ApiViewHandler):

    @login_required
    def post(self):
        req_file = request.files.get('file')
        if not req_file:
            raise VerifyError('Couldn\'t find any uploaded file')
        df = pd.read_excel(
            io.BytesIO(req_file.read()),
        )
        return replace_nan(df.to_dict(orient='records'))


class NavUpdateAPI(ApiViewHandler):

    @login_required
    def post(self, fof_id):
        method = request.json.get('method', 'part')
        nav_data = request.json.get('nav_data', [])
        if not nav_data:
            return

        dates = []
        for i in nav_data:
            i['日期'] = datetime.datetime.strptime(i.get('日期'), '%Y-%m-%d').date()
            dates.append(i['日期'])

        if method == 'part':

            db.session.query(
                FOFNav
            ).filter(
                FOFNav.fof_id == fof_id,
                FOFNav.manager_id == g.token.manager_id,
                FOFNav.datetime.in_(dates),
            ).delete(synchronize_session=False)

            for i in nav_data:
                new = FOFNav(
                    fof_id=fof_id,
                    nav=i['单位净值'],
                    acc_net_value=i.get('累计净值'),
                    datetime=i['日期'],
                    manager_id=g.token.manager_id,
                )
                db.session.add(new)
            db.session.commit()

        if method == 'all':
            db.session.query(
                FOFNav
            ).filter(
                FOFNav.fof_id == fof_id,
                FOFNav.manager_id == g.token.manager_id,
            ).delete(synchronize_session=False)

            for i in nav_data:
                new = FOFNav(
                    fof_id=fof_id,
                    nav=i['单位净值'],
                    acc_net_value=i['累计净值'],
                    datetime=i['日期'],
                    manager_id=g.token.manager_id,
                )
                db.session.add(new)
            db.session.commit()

        results = db.session.query(
            FOFNav
        ).filter(
            FOFNav.fof_id == fof_id,
            FOFNav.manager_id == g.token.manager_id,
        ).all()
        if len(results) < 2:
            return

        df = pd.DataFrame([i.to_dict() for i in results])
        df = df.rename(columns={
            'nav': 'net_asset_value',
            'acc_net_value': 'acc_unit_value'
        })

        dff = HedgeFundDataManager.calc_whole_adjusted_net_value(df)
        for i, j in enumerate(results):
            j.adjusted_nav = float(dff.loc[i, 'adj_nav']) if dff.loc[i, 'adj_nav'] else None
        db.session.commit()
        try:
            obj = FOFInfo.filter_by_query(
                fof_id=fof_id,
                manager_id=g.token.manager_id,
            ).first()
            if not obj:
                return

            df['adj_nav'] = dff['adj_nav']
            ratios = Calculator.get_stat_result_from_df(df, 'datetime', 'adj_nav')
            obj.ret_year_to_now = float(replace_nan(ratios.recent_year_ret))
            obj.ret_total = float(ratios.last_unit_nav - 1)
            obj.ret_ann = float(ratios.annualized_ret) if ratios.annualized_ret else None
            obj.mdd = float(ratios.mdd) if ratios.mdd else None
            obj.sharpe = float(ratios.sharpe) if ratios.sharpe else None
            obj.vol = float(ratios.annualized_vol) if ratios.annualized_vol else None
            obj.latest_cal_date = ratios.end_date
            obj.net_asset_value = float(df.iloc[-1]['net_asset_value'])
            obj.acc_unit_value = float(df.iloc[-1]['acc_unit_value'])
            obj.adjusted_net_value = float(df.iloc[-1]['adj_nav'])
            obj.save()

        except Exception as e:
            print(traceback.format_exc())
            pass

        return


class NavByDateAPI(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        date = request.args.get('date')
        if not date:
            return
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        obj = FOFNav.filter_by_query(
            fof_id=fof_id,
            datetime=date,
        ).first()
        if not obj:
            return {}

        return obj.to_dict()
