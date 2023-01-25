# Pydantic
from pydantic import BaseModel, Field

# Python
from typing import List

# Roles and Permissions
from schemas.lov    import IdLov
from schemas.schema import BaseModels, GetModel, DescriptionModel, IdModel, SkillModel


class IdLovVals(BaseModel):
    lovvals_id: int = Field(
        ...,
        example = 1,
        gt = 0
    )


class BaseLovVals(IdLov, BaseModels, SkillModel):
    pass


class SaveLovVals(BaseLovVals, DescriptionModel):
    pass


class GetLovVal(IdModel, SaveLovVals):
    class Config:
        orm_mode = True


class GetLovVals(GetLovVal):
    lov: GetModel
    class Config:
        orm_mode = True


class GetInfoLovVals(GetModel):
    lov_vals: List[GetLovVal]


class UpdateSkillLovVals(DescriptionModel, SkillModel):
    pass