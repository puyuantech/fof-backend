
from bases.globals import db
from models import ManagementFund, FOFInfo


def extend_fof_info_from_management():
    funds = db.session.query(
        ManagementFund.fund_no,
        ManagementFund.fund_name,
    ).filter(ManagementFund.fund_no.isnot(None))
    funds = {fund_no: fund_name for fund_no, fund_name in funds}

    fofs = db.session.query(FOFInfo.fof_id.distinct()).all()
    fofs = set(fof_id for fof_id, in fofs)

    to_add = funds.keys() - fofs
    print(f'to_add: {len(to_add)}')

    for fund_no in to_add:
        fund_name = funds[fund_no]
        FOFInfo(
            fof_id=fund_no,
            manager_id='1',
            fof_name=fund_name,
        ).save(commit=False)

    db.session.commit()
    print('done!')
