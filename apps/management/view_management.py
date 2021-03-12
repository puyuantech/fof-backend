
from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from models import Management, ManagementFund, ManagementSenior, ManagementRelatedParty, ManagementInvestor
from utils.decorators import login_required
from utils.helper import generate_sql_pagination


class ManagementAPI(ApiViewHandler):

    @login_required
    def get(self, manager_id):
        management = Management.get_by_query(manager_id=manager_id)
        data = management.to_dict(remove_fields_list={'fund_ids'})
        data.update({
            'funds': ManagementFund.get_funds(management.fund_ids),
            'seniors': ManagementSenior.get_seniors(management.manager_id),
            'related_parties': ManagementRelatedParty.get_related_parties(management.manager_id),
            'investors': ManagementInvestor.get_investors(management.manager_id),
        })
        return data


class ManagementListAPI(ApiViewHandler):

    @login_required
    def get(self):
        p = generate_sql_pagination()
        query = Management.filter_by_query()
        return p.paginate(query, call_back=lambda x: [i.to_list_dict() for i in x])

    @login_required
    def post(self):
        query_dict = {}
        if self.input.manager_name:
            query_dict['manager_name'] = self.input.manager_name
        if self.input.register_no:
            query_dict['register_no'] = self.input.register_no
        if not query_dict:
            raise LogicError('缺少查询参数!')
        managements = Management.filter_by_query(**query_dict).all()
        return [management.to_list_dict() for management in managements]


class ManagementFundAPI(ApiViewHandler):

    @login_required
    def get(self, fund_id):
        fund = ManagementFund.get_by_query(fund_id=fund_id)
        data = fund.to_dict(remove_fields_list={'manager_ids'})

        managements = Management.filter_by_query().filter(Management.manager_id.in_(fund.manager_ids)).all()
        data['managements'] = [management.to_dict(remove_fields_list={'fund_ids'}) for management in managements]
        return data

