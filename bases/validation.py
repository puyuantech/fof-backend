from pydantic import BaseModel, ValidationError, constr

from bases.exceptions import ParamsError


class BaseValidation(BaseModel):

    @classmethod
    def get_valid_data(cls, input: dict):
        try:
            validation = cls.parse_obj(input)
        except ValidationError as e:
            raise ParamsError(str(e))
        return validation.dict()


class InvestorValidation(BaseValidation):
    investor_id: constr(max_length=32)


class ManagerValidation(BaseValidation):
    manager_id: constr(max_length=32)


class UnitValidation(BaseValidation):
    investor_id: constr(max_length=32)
    manager_id: constr(max_length=32)


class ContractValidation(BaseValidation):
    investor_id: constr(max_length=32)
    manager_id: constr(max_length=32)
    fof_id: constr(max_length=16)

