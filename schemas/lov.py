from pydantic import BaseModel, Field


class IdLov(BaseModel):
    lov_id: int = Field(
        ...,
        example = 1,
        gt      = 0
    )