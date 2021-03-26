from bases.globals import db, settings
from models import FOFInfo, ManagementFund
from apps import create_app
import traceback
create_app().app_context().push()


def migrate_hedge_to_fof():
    objs = ManagementFund.filter_by_query().all()
    print(len(objs))
    j = 0
    for i in objs:
        if j <= 1000:
            new = FOFInfo(
                fof_id=i.fund_no,
                fof_name=i.fund_name,
                fund_no=i.fund_no,
                established_date=i.establish_date,
                filing_date=i.filing_date,
                filing_stage=i.filing_stage,
                fund_type=i.fund_type,
                currency_type=i.currency_type,
                management_type=i.management_type,
                custodian_name=i.custodian_name,
                fund_status=i.fund_status,
                management_ids=i.manager_ids,
                manager_id='1',
                asset_type='fund',
                fof_status='',
                subscription_fee = 0,
                redemption_fee = 0,
                management_fee = 0,
                custodian_fee = 0,
                administrative_fee = 0,
                lock_up_period = '',
                incentive_fee_mode = '',
                incentive_fee = '',
                datetime='',
                admin='',
            )
            db.session.add(new)
            j += 1
        else:
            j = 0
            try:
                db.session.commit()
                print('success')
            except Exception as e:
                db.session.rollback()
                print(traceback.format_exc())
                print(i)


if __name__ == '__main__':
    migrate_hedge_to_fof()


