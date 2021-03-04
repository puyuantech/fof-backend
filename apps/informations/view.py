
from bases.view_mixin import *
from bases.viewhandler import ApiViewHandler
from models import InfoDetail, InfoTemplate


class InformationAPI(ApiViewHandler, ViewList, ViewUpdate):
    model = InfoDetail


class InformationDetailAPI(ApiViewHandler, ViewDetailGet, ViewDetailPut, ViewDetailDelete):
    model = InfoDetail


class TemplateAPI(ApiViewHandler, ViewList, ViewUpdate):
    model = InfoTemplate


class TemplateDetailAPI(ApiViewHandler, ViewDetailGet, ViewDetailPut, ViewDetailDelete):
    model = InfoTemplate
