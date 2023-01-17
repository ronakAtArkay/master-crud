from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from libs.utils import generate_id, now
from models import CityModel, StateModel
from routers.admin.v1.schemas import CityAdd


def add_city(city_schema: CityAdd, db: Session):
    id = generate_id()
    db_city = CityModel(id=id, name=city_schema.name, state_id=city_schema.state_id)
    db_state = (
        db.query(StateModel)
        .filter(StateModel.id == city_schema.state_id, StateModel.is_deleted == False)
        .first()
    )
    if db_state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="state is not found"
        )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city_by_id(city_id: str, db: Session):
    return (
        db.query(CityModel)
        .filter(CityModel.id == city_id, CityModel.is_deleted == False)
        .first()
    )


def get_city(city_id: str, db: Session):
    db_city = get_city_by_id(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="city is not found"
        )
    return db_city


def get_city_list(
    start: int,
    limit: int,
    sort_by: str,
    order: str,
    search: str,
    state_id: str,
    db: Session,
):
    query = db.query(CityModel).filter(CityModel.is_deleted == False)

    if state_id != "all":
        query = query.filter(
            CityModel.state_id == state_id, CityModel.is_deleted == False
        )

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(or_(CityModel.name.like(text)))

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(CityModel.name.desc())
        else:
            query = query.order_by(CityModel.name)
    else:
        query = query.order_by(CityModel.updated_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data


def get_all_city(state_id: str, db: Session):
    query = db.query(CityModel)

    if state_id != "all":
        query = query.filter(
            CityModel.state_id == state_id, CityModel.is_deleted == False
        )
    else:
        query = query.filter(CityModel.is_deleted == False)

    db_city = query.order_by(CityModel.created_at.desc()).all()
    return db_city


def update_city(city_schema: CityAdd, city_id: str, db: Session):
    db_city = get_city_by_id(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City is not found"
        )
    db_state = (
        db.query(StateModel)
        .filter(StateModel.id == city_schema.state_id, StateModel.is_deleted == False)
        .first()
    )
    if db_state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State is not found"
        )
    db_city.name = city_schema.name
    db_city.state_id = city_schema.state_id
    db_city.updated_at = now()
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(city_id: str, db: Session):
    db_city = get_city_by_id(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="city Not found"
        )
    db_city.is_deleted = True
    db_city.updated_at = now()
    db.commit()
    db.refresh(db_city)
    return f"{db_city.name} is deleted successfully"
