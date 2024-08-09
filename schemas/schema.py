from datetime   import datetime
from pydantic   import BaseModel, Field
from typing     import Any, Optional


class IdModel(BaseModel):
    id: int = Field(
        ...,
        example = 1,
        gt = 0
    )


class DescriptionModel(BaseModel):
    description: str = Field(
        ...,
        min_length  = 1,
        max_length  = 100,
        example     = "Detalle"
    )


class ActiveModel(BaseModel):
    active: bool = Field(
        ...,
        example = True
    )


class CreateModel(BaseModel):
    created_at: datetime = Field(...)


class CommentModel(BaseModel):
    comment: Optional[str] = Field(
        default = None,
        example = "Descripción del valor"
    )


class SkillModel(BaseModel):
    skill: Optional[Any] = Field(
        default = None,
        example = {}
    )


class BaseModels(ActiveModel, CreateModel, CommentModel):
    pass


class SaveModel(DescriptionModel, BaseModels, SkillModel):
    pass


class UpdateDescriptionModel(IdModel, DescriptionModel):
    pass


class GetModel(IdModel, SaveModel, SkillModel):
    class Config: 
        from_attributes=True