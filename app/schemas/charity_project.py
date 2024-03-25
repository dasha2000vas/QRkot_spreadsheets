from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, PositiveInt, validator
)

MAX_LENGTH = 100
MIN_LENGTH = 1


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=MAX_LENGTH)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = MIN_LENGTH
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @validator('name', 'description')
    def name_and_description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название и описание проекта не могут быть пустыми!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
