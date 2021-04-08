from surfing.data.view.basic_models import FOFInfo as SurfingFOFInfo
from surfing.data.view.basic_models import HedgeFundNAV as SurfingHedgeFundNAV
from surfing.data.view.basic_models import FOFScaleAlteration as SurfingFOFScaleAlteration
from surfing.data.view.basic_models import FOFAssetAllocation as SurfingFOFAssetAllocation
from surfing.data.view.basic_models import FOFManually as SurfingFOFManually
from surfing.data.view.basic_models import FOFInvestorPosition as SurfingFOFInvestorPosition
from surfing.data.view.basic_models import HedgeFundInfo as SurfingHedgeFundInfo
from surfing.data.view.basic_models import FOFAccountStatement as SurfingFOFAccountStatement
from surfing.data.view.basic_models import FOFTransitMoney as SurfingFOFTransitMoney
from surfing.data.view.basic_models import FOFEstimateInterest as SurfingFOFEstimateInterest
from surfing.data.view.basic_models import FOFEstimateFee as SurfingFOFEstimateFee
from surfing.data.view.basic_models import FOFOtherRecord as SurfingFOFOtherRecord
from surfing.data.view.basic_models import MngInfo as SurfingMngInfo
from surfing.data.view.basic_models import FOFIncidentalStatement as SurfingFOFIncidentalStatement
from surfing.data.view.basic_models import FOFRealAccountStatement as SurfingFOFRealAccountStatement
from surfing.data.view.basic_models import FOFRealTransitMoney as SurfingFOFRealTransitMoney
from surfing.data.view.basic_models import FOFRealEstimateInterest as SurfingFOFRealEstimateInterest
from surfing.data.view.basic_models import FOFRealEstimateFee as SurfingFOFRealEstimateFee
from surfing.data.view.basic_models import FOFInvestorPositionSummary as SurfingFOFInvestorPositionSummary

from surfing.data.view.derived_models import FOFPosition as SurfingFOFPosition
from surfing.data.view.derived_models import FOFNav as SurfingFOFNav
from surfing.data.view.derived_models import FOFNavCalc as SurfingFOFNavCalc
from surfing.data.view.derived_models import FOFNavPublic as SurfingFOFNavPublic
from surfing.data.view.derived_models import FOFPositionDetail as SurfingFOFPositionDetail
from surfing.data.view.derived_models import FOFInvestorData as SurfingFOFInvestorData
from surfing.data.view.derived_models import HedgeFundInvestorPurAndRedemp as SurfingHedgeFundInvestorPurAndRedemp
from surfing.data.view.derived_models import HedgeFundInvestorDivAndCarry as SurfingHedgeFundInvestorDivAndCarry
from surfing.data.view.derived_models import HedgeFundInvestorPurAndRedempSub as SurfingHedgeFundInvestorPurAndRedempSub
from surfing.data.view.derived_models import HedgeFundCustodianData as SurfingHedgeFundCustodianData


from bases.dbwrapper import BaseModel, db


class MngInfo(SurfingMngInfo, db.Model):
    __bind_key__ = 'basic'


class HedgeFundNAV(SurfingHedgeFundNAV, BaseModel):
    __tablename__ = 'hedge_fund_nav'
    __bind_key__ = 'basic'
    __table_args__ = {
        'extend_existing': True,
    }


class FOFInfo(SurfingFOFInfo, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFScaleAlteration(SurfingFOFScaleAlteration, BaseModel):
    __tablename__ = 'fof_scale_alteration'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFAssetAllocation(SurfingFOFAssetAllocation, BaseModel):
    __tablename__ = 'fof_asset_allocation'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFManually(SurfingFOFManually, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFInvestorPosition(SurfingFOFInvestorPosition, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class HedgeFundInfo(SurfingHedgeFundInfo, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFPosition(SurfingFOFPosition, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFNav(SurfingFOFNav, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFNavPublic(SurfingFOFNavPublic, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFNavCalc(SurfingFOFNavCalc, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFIncidentalStatement(SurfingFOFIncidentalStatement, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFAccountStatement(SurfingFOFAccountStatement, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFTransitMoney(SurfingFOFTransitMoney, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFEstimateInterest(SurfingFOFEstimateInterest, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFEstimateFee(SurfingFOFEstimateFee, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFRealAccountStatement(SurfingFOFRealAccountStatement, BaseModel):
    __tablename__ = 'fof_account_statement_real'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFRealTransitMoney(SurfingFOFRealTransitMoney, BaseModel):
    __tablename__ = 'fof_transit_money_real'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFRealEstimateInterest(SurfingFOFRealEstimateInterest, BaseModel):
    __tablename__ = 'fof_estimate_interest_real'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFRealEstimateFee(SurfingFOFRealEstimateFee, BaseModel):
    __tablename__ = 'fof_estimate_fee_real'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFOtherRecord(SurfingFOFOtherRecord, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFInvestorPositionSummary(SurfingFOFInvestorPositionSummary, BaseModel):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFPositionDetail(SurfingFOFPositionDetail, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFInvestorData(SurfingFOFInvestorData, BaseModel):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class HedgeFundInvestorPurAndRedemp(SurfingHedgeFundInvestorPurAndRedemp, BaseModel):
    __tablename__ = 'hedge_fund_investor_pur_redemp'
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class HedgeFundInvestorDivAndCarry(SurfingHedgeFundInvestorDivAndCarry, BaseModel):
    __tablename__ = 'hedge_fund_investor_div_carry'
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class HedgeFundInvestorPurAndRedempSub(SurfingHedgeFundInvestorPurAndRedempSub, BaseModel):
    __tablename__ = 'hedge_fund_investor_pur_redemp_sub'
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class HedgeFundCustodianData(SurfingHedgeFundCustodianData, BaseModel):
    __tablename__ = 'hedge_fund_custodian_data'
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}
