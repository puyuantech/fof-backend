
from bases.viewhandler import ApiViewHandler
from models import Management, ManagementFund
from utils.decorators import login_required
from utils.helper import generate_sql_pagination


class ManagementAPI(ApiViewHandler):

    @login_required
    def get(self, manager_id):
        management = Management.get_by_query(manager_id=manager_id)
        data = management.to_dict(remove_fields_list={'fund_ids'})

        funds = ManagementFund.filter_by_query().filter(ManagementFund.fund_id.in_(management.fund_ids)).all()
        data['funds'] = [fund.to_dict(remove_fields_list={'manager_ids'}) for fund in funds]
        return data


class ManagementListAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = Management.filter_by_query()
        return p.paginate(query, call_back=lambda x: [i.to_list_dict() for i in x])


class ManagementFundAPI(ApiViewHandler):

    @login_required
    def get(self, fund_id):
        fund = ManagementFund.get_by_query(fund_id=fund_id)
        data = fund.to_dict(remove_fields_list={'manager_ids'})

        managements = Management.filter_by_query().filter(Management.manager_id.in_(fund.manager_ids)).all()
        data['managements'] = [management.to_dict(remove_fields_list={'fund_ids'}) for management in managements]
        return data

