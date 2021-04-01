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

