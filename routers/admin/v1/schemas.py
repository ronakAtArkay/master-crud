from typing import List, Optional

from pydantic import BaseModel, Field


class SeaRegionAdd(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class SeaRegion(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class SeaRegionList(BaseModel):
    count: int
    list: List[SeaRegion]

    class Config:
        orm_mode = True


class CountryAdd(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    sea_region_id: Optional[str] = Field(min_length=36, max_length=36)


class Country(BaseModel):
    id: str
    name: str
    sea_region: SeaRegion

    class Config:
        orm_mode = True


class CountryList(BaseModel):
    count: int
    list: List[Country]

    class Config:
        orm_mode = True


class StateAdd(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    country_id: Optional[str] = Field(min_length=36, max_length=36)


class State(BaseModel):
    id: str
    name: str
    country: Country

    class Config:
        orm_mode = True


class StateList(BaseModel):
    count: int
    list: List[State]

    class Config:
        orm_mode = True


class CityAdd(BaseModel):
    name: str = Field(..., min_length=2, max_length=36)
    state_id: Optional[str] = Field(min_length=36, max_length=36)


class City(BaseModel):
    id: str
    name: str
    state: State

    class Config:
        orm_mode = True


class CityList(BaseModel):
    count: int
    list: List[City]

    class Config:
        orm_mode = True
