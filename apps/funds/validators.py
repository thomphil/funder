from datetime import date, datetime
from typing import Iterable, Optional, Union

from pydantic import validator, BaseModel
from pydantic.validators import str_validator


def empty_to_none(v: str) -> Optional[str]:
    if v == '':
        return None
    return v


class EmptyStrToNone(str):
    """
    If AUM is passed an empty string it will be invalid as it can't cast it to an int
    so we need to check for that and convert these to None
    """
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


class BaseModelExt(BaseModel):
    """
    BaseModel instances require kwargs to be passed to the constructor
    this adds functionality to allow positional args to initialise the model
    """
    @classmethod
    def parse_args(cls, values: Iterable):
        return cls.parse_obj(dict(zip(cls.__fields__, values)))


class FundCSVRow(BaseModelExt):
    name: str
    strategy: str
    aum: Union[None, int, EmptyStrToNone]
    inception_date: Union[None, date]

    @validator('name')
    def name_is_not_blank(cls, v):
        if not v:
            raise ValueError('Name cannot be blank')
        return v
    
    @validator('strategy')
    def strategy_is_valid_choice(cls, value):
        from .models import STRATEGY_CHOICES

        if value not in dict(STRATEGY_CHOICES).values():
            raise ValueError('strategy is not a valid choice')
        return value

    @validator('aum')
    def aum_is_positive(cls, value):
        if value == "":
            return None

        if value and value < 0:
            raise ValueError('aum must be positive if present')
        return value

    @validator("inception_date", pre=True)
    def parse_inception_date(cls, value):
        if value == "":
            return None

        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()
