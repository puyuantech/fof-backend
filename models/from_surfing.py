from surfing.data.view.basic_models import FOFInfo as SurfingFOFInfo
from surfing.data.view.basic_models import HedgeFundNAV as SurfingHedgeFundNAV
from surfing.data.view.basic_models import FOFScaleAlteration as SurfingFOFScaleAlteration
from surfing.data.view.basic_models import FOFAssetAllocation as SurfingFOFAssetAllocation
from surfing.data.view.basic_models import FOFManually as SurfingFOFManually
from surfing.data.view.basic_models import FOFInvestorPosition as SurfingFOFInvestorPosition
from surfing.data.view.basic_models import HedgeFundInfo as SurfingHedgeFundInfo
from surfing.data.view.basic_models import MngInfo as SurfingMngInfo
from surfing.data.view.derived_models import FOFPosition as SurfingFOFPosition
from surfing.data.view.derived_models import FOFNav as SurfingFOFNav

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

