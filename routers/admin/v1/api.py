from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from dependencies import get_db
from routers.admin.v1.crud import city, countries, sea_region, state
from routers.admin.v1.schemas import (
    City,
    CityAdd,
    CityList,
    Country,
    CountryAdd,
    CountryList,
    SeaRegion,
    SeaRegionAdd,
    SeaRegionList,
    State,
    StateAdd,
    StateList,
)

router = APIRouter()

# sea-region


@router.post("/sea_region", status_code=status.HTTP_201_CREATED, tags=["sea_region"])
def add_sea_region(region_schema: SeaRegionAdd, db: Session = Depends(get_db)):
    data = sea_region.add_sea_region(region_schema=region_schema, db=db)
    return data


@router.get("/sea_region/{region_id}", response_model=SeaRegion, tags=["sea_region"])
def get_sea_region(
    region_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = sea_region.get_sea_region(region_id=region_id, db=db)
    return data


@router.get("/sea_region", response_model=SeaRegionList, tags=["sea_region"])
def get_region_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    data = sea_region.get_region_list(
        start=start, limit=limit, sort_by=sort_by, order=order, search=search, db=db
    )
    return data


@router.get("/sea_region/all/", response_model=List[SeaRegion], tags=["sea_region"])
def get_all_sea_region(db: Session = Depends(get_db)):
    data = sea_region.get_all_sea_region(db=db)
    return data


@router.put("/sea_region/{region_id}", response_model=SeaRegion, tags=["sea_region"])
def update_sea_region(
    region_schema: SeaRegionAdd,
    region_id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = sea_region.update_sea_region(
        region_schema=region_schema, region_id=region_id, db=db
    )
    return data


@router.delete("/sea_region/{region_id}", tags=["sea_region"])
def delete_sea_region(
    region_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = sea_region.delete_sea_region(region_id=region_id, db=db)
    return data


# end sea-region

# country


@router.post("/countries", status_code=status.HTTP_201_CREATED, tags=["country"])
def add_country(country_schema: CountryAdd, db: Session = Depends(get_db)):
    data = countries.add_country(country_schema=country_schema, db=db)
    return data


@router.get("/countries/{country_id}", response_model=Country, tags=["country"])
def get_country(
    country_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = countries.get_country(country_id=country_id, db=db)
    return data


@router.get("/countries", response_model=CountryList, tags=["country"])
def get_country_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    sea_region_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = countries.get_countries_list(
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
        db=db,
        sea_region_id=sea_region_id,
    )
    return data


@router.get("/countries/all/", response_model=List[Country], tags=["country"])
def get_all_country(
    sea_region_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = countries.get_all_countries(sea_region_id=sea_region_id, db=db)
    return data


@router.put("/countries/{country_id}", response_model=Country, tags=["country"])
def update_country(
    country_schema: CountryAdd,
    country_id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = countries.update_country(
        country_schema=country_schema, country_id=country_id, db=db
    )
    return data


@router.delete("/countries/{country_id}", tags=["country"])
def delete_country(
    country_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = countries.delete_country(country_id=country_id, db=db)
    return data


# end country

# state


@router.post("/state", status_code=status.HTTP_201_CREATED, tags=["state"])
def add_state(state_schema: StateAdd, db: Session = Depends(get_db)):
    data = state.add_state(state_schema=state_schema, db=db)
    return data


@router.get("/state/{state_id}", response_model=State, tags=["state"])
def get_state(
    state_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = state.get_state(state_id=state_id, db=db)
    return data


@router.get("/state", response_model=StateList, tags=["state"])
def get_state_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    country_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = state.get_state_list(
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
        country_id=country_id,
        db=db,
    )
    return data


@router.get("/state/all/", response_model=List[State], tags=["state"])
def get_all_state(
    country_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = state.get_all_state(country_id=country_id, db=db)
    return data


@router.put("/state/{state_id}", response_model=State, tags=["state"])
def update_state(
    state_schema: StateAdd,
    state_id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = state.update_state(state_schema=state_schema, state_id=state_id, db=db)
    return data


@router.delete("/state/{state_id}", tags=["state"])
def delete_state(
    state_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = state.delete_state(state_id=state_id, db=db)
    return data


# end state

# city


@router.post("/city", status_code=status.HTTP_201_CREATED, tags=["city"])
def add_city(city_schema: CityAdd, db: Session = Depends(get_db)):
    data = city.add_city(city_schema=city_schema, db=db)
    return data


@router.get("/city/{city_id}", response_model=City, tags=["city"])
def get_city(
    city_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = city.get_city(city_id=city_id, db=db)
    return data


@router.get("/city", response_model=CityList, tags=["city"])
def get_city_list(
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    state_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = city.get_city_list(
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
        state_id=state_id,
        db=db,
    )
    return data


@router.get("/city/all/", response_model=List[City], tags=["city"])
def get_all_city(
    state_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db),
):
    data = city.get_all_city(state_id=state_id, db=db)
    return data


@router.put("/city/{city_id}", response_model=City, tags=["city"])
def update_city(
    city_schema: CityAdd,
    city_id: str = Path(min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    data = city.update_city(city_schema=city_schema, city_id=city_id, db=db)
    return data


@router.delete("/city/{city_id}", tags=["city"])
def delete_city(
    city_id: str = Path(min_length=36, max_length=36), db: Session = Depends(get_db)
):
    data = city.delete_city(city_id=city_id, db=db)
    return data
