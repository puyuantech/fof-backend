import pandas as pd
import io
import datetime
from flask import make_response, request
from bases.viewhandler import ApiViewHandler
from bases.exceptions import VerifyError
from bases.globals import db
from models import FOFNav
from utils.decorators import login_required
from utils.helper import replace_nan


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
                FOFNav.datetime.in_(dates),
            ).delete(synchronize_session=False)

            for i in nav_data:
                new = FOFNav(
                    fof_id=fof_id,
                    nav=i['单位净值'],
                    acc_net_value=i.get('累计净值'),
                    datetime=i['日期'],
                )
                db.session.add(new)
            db.session.commit()

        if method == 'all':
            db.session.query(
                FOFNav
            ).filter(
                FOFNav.fof_id == fof_id,
            ).delete(synchronize_session=False)

            for i in nav_data:
                new = FOFNav(
                    fof_id=fof_id,
                    nav=i['单位净值'],
                    acc_net_value=i['累计净值'],
                    datetime=i['日期'],
                )
                db.session.add(new)
            db.session.commit()

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
