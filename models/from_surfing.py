from surfing.data.view.basic_models import FOFInfo as SurfingFOFInfo
from surfing.data.view.basic_models import FOFScaleAlteration as SurfingFOFScaleAlteration
from surfing.data.view.basic_models import FOFAssetAllocation as SurfingFOFAssetAllocation
from surfing.data.view.basic_models import FOFManually as SurfingFOFManually
from surfing.data.view.basic_models import FOFInvestorPosition as SurfingFOFInvestorPosition
from surfing.data.view.basic_models import StockTag as SurfingStockTag
from surfing.data.view.basic_models import HedgeFundInfo as SurfingHedgeFundInfo
from surfing.data.view.basic_models import HedgeFundNAV as SurfingHedgeFundNAV
from surfing.data.view.derived_models import FOFPosition as SurfingFOFPosition
from surfing.data.view.derived_models import FOFNav as SurfingFOFNav

from bases.dbwrapper import db, DBMixin


class StockTag(SurfingStockTag, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFInfo(SurfingFOFInfo, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFScaleAlteration(SurfingFOFScaleAlteration, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFAssetAllocation(SurfingFOFAssetAllocation, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFManually(SurfingFOFManually, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFInvestorPosition(SurfingFOFInvestorPosition, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class HedgeFundInfo(SurfingHedgeFundInfo, DBMixin, db.Model):
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class HedgeFundNAV(SurfingHedgeFundNAV, DBMixin, db.Model):
    __bind_key__ = 'basic'


class FOFPosition(SurfingFOFPosition, DBMixin, db.Model):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}


class FOFNav(SurfingFOFNav, DBMixin, db.Model):
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}
