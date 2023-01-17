from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from libs.utils import generate_id, now
from models import CountryModel, SeaRegionModel, StateModel
from routers.admin.v1.schemas import CountryAdd


def get_country_by_id(country_id: str, db: Session):
    return (
        db.query(CountryModel)
        .filter(CountryModel.id == country_id, CountryModel.is_deleted == False)
        .first()
    )


def add_country(country_schema: CountryAdd, db: Session):
    id = generate_id()
    db_countries = CountryModel(
        id=id,
        name=country_schema.name,
        sea_region_id=country_schema.sea_region_id,
    )
    db_region = (
        db.query(SeaRegionModel)
        .filter(
            SeaRegionModel.id == country_schema.sea_region_id,
            SeaRegionModel.is_deleted == False,
        )
        .first()
    )
    if db_region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sea-Region is Not Found"
        )
    db.add(db_countries)
    db.commit()
    db.refresh(db_countries)
    return db_countries


def get_country(country_id: str, db: Session):
    db_countries = get_country_by_id(country_id=country_id, db=db)
    if db_countries is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country is not found"
        )
    return db_countries


def get_countries_list(
    start: int,
    limit: int,
    sort_by: str,
    order: str,
    search: str,
    sea_region_id: str,
    db: Session,
):
    query = db.query(CountryModel).filter(CountryModel.is_deleted == False)

    if sea_region_id != "all":
        query = query.filter(
            CountryModel.sea_region_id == sea_region_id,
            CountryModel.is_deleted == False,
        )

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(or_(CountryModel.name.like(text)))

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(CountryModel.name.desc())
        else:
            query = query.order_by(CountryModel.name)

    else:
        query = query.order_by(CountryModel.updated_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data


def get_all_countries(sea_region_id: str, db: Session):
    query = db.query(CountryModel)

    if sea_region_id != "all":
        query = query.filter(
            CountryModel.sea_region_id == sea_region_id,
            CountryModel.is_deleted == False,
        )
    else:
        query = query.filter(CountryModel.is_deleted == False)
    db_countries = query.order_by(CountryModel.created_at.desc()).all()
    return db_countries


def update_country(country_id: str, db: Session, country_schema: CountryAdd):
    db_countries = get_country_by_id(country_id=country_id, db=db)
    if db_countries is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country is Not Found"
        )
    db_region = (
        db.query(SeaRegionModel)
        .filter(
            SeaRegionModel.id == country_schema.sea_region_id,
            SeaRegionModel.is_deleted == False,
        )
        .first()
    )
    if db_region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sea-Region is Not Found"
        )
    db_countries.name = country_schema.name
    db_countries.updated_at = now()
    db.commit()
    db.refresh(db_countries)
    return db_countries


def delete_country(country_id: str, db: Session):
    db_countries = get_country_by_id(country_id=country_id, db=db)
    if db_countries is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country is Not Found"
        )
    count = (
        db.query(StateModel.id)
        .filter(StateModel.country_id == country_id, StateModel.is_deleted == False)
        .count()
    )
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Country has state"
        )
    db_countries.is_deleted = True
    db_countries.updated_at = now()
    db.commit()
    db.refresh(db_countries)
    return f"{db_countries.name} is deleted successfully"
