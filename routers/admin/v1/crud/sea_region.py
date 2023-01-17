from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from libs.utils import generate_id, now
from models import CountryModel, SeaRegionModel
from routers.admin.v1.schemas import SeaRegionAdd


def add_sea_region(region_schema: SeaRegionAdd, db: Session):
    id = generate_id()
    db_region = SeaRegionModel(id=id, name=region_schema.name)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region


def get_region_by_id(region_id: str, db: Session):
    return (
        db.query(SeaRegionModel)
        .filter(SeaRegionModel.id == region_id, SeaRegionModel.is_deleted == False)
        .first()
    )


def get_sea_region(region_id: str, db: Session):
    db_region = get_region_by_id(region_id=region_id, db=db)
    if db_region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sea-Region is Not Found"
        )
    return db_region


def get_region_list(
    start: int, limit: int, sort_by: str, order: str, search: str, db: Session
):
    query = db.query(SeaRegionModel).filter(SeaRegionModel.is_deleted == False)

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(or_(SeaRegionModel.name.like(text)))

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(SeaRegionModel.name.desc())
        else:
            query = query.order_by(SeaRegionModel.name)
    else:
        query = query.order_by(SeaRegionModel.updated_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data


def get_all_sea_region(db: Session):
    query = (
        db.query(SeaRegionModel)
        .filter(SeaRegionModel.is_deleted == False)
        .order_by(SeaRegionModel.name.desc())
        .all()
    )
    return query


def update_sea_region(region_id: str, db: Session, region_schema: SeaRegionAdd):
    db_region = get_region_by_id(region_id=region_id, db=db)
    if db_region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sea-region is Not Found"
        )
    db_region.name = region_schema.name
    db_region.updated_at = now()
    db.commit()
    db.refresh(db_region)
    return db_region


def delete_sea_region(region_id: str, db: Session):
    db_region = get_region_by_id(region_id=region_id, db=db)
    if db_region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sea-region is Not Found"
        )
    count = (
        db.query(CountryModel.id)
        .filter(
            CountryModel.sea_region_id == region_id, CountryModel.is_deleted == False
        )
        .count()
    )
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sea_region has country"
        )
    db_region.is_deleted = True
    db_region.updated_at = now()
    db.commit()
    db.refresh(db_region)
    return f"{db_region.name} is deleted successfully"
