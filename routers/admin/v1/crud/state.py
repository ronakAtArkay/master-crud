from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from libs.utils import generate_id, now
from models import CityModel, CountryModel, StateModel
from routers.admin.v1.schemas import StateAdd


def add_state(state_schema: StateAdd, db: Session):
    id = generate_id()
    db_state = StateModel(
        id=id, name=state_schema.name, country_id=state_schema.country_id
    )
    db_country = (
        db.query(CountryModel)
        .filter(
            CountryModel.id == state_schema.country_id, CountryModel.is_deleted == False
        )
        .first()
    )
    if db_country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country is not found"
        )
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


def get_state_by_id(state_id: str, db: Session):
    return (
        db.query(StateModel)
        .filter(StateModel.id == state_id, StateModel.is_deleted == False)
        .first()
    )


def get_state(state_id: str, db: Session):
    query = get_state_by_id(state_id=state_id, db=db)
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State not found"
        )
    return query


def get_state_list(
    start: int,
    limit: int,
    sort_by: str,
    order: str,
    search: str,
    country_id: str,
    db: Session,
):
    query = db.query(StateModel).filter(StateModel.is_deleted == False)

    if country_id != "all":
        query = query.filter(
            StateModel.country_id == country_id, StateModel.is_deleted == False
        )

    if search != "all":
        text = f"""%{search}%"""
        query = query.filter(or_(StateModel.name.like(text)))

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(StateModel.name.desc())
        else:
            query = query.order_by(StateModel.name)

    else:
        query = query.order_by(StateModel.updated_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data


def get_all_state(country_id: str, db: Session):
    query = db.query(StateModel)

    if country_id != "all":
        query = query.filter(
            StateModel.country_id == country_id, StateModel.is_deleted == False
        )
    else:
        query = query.filter(StateModel.is_deleted == False)
    db_state = query.order_by(StateModel.created_at.desc()).all()
    return db_state


def update_state(state_schema: StateAdd, state_id: str, db: Session):
    db_state = get_state_by_id(state_id=state_id, db=db)
    if db_state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State is not found"
        )
    db_country = (
        db.query(CountryModel)
        .filter(
            CountryModel.id == state_schema.country_id, CountryModel.is_deleted == False
        )
        .first()
    )
    if db_country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="country is not found"
        )
    db_state.name = state_schema.name
    db_state.country_id = state_schema.country_id
    db_state.updated_at = now()
    db.commit()
    db.refresh(db_state)
    return db_state


def delete_state(state_id: str, db: Session):
    db_state = get_state_by_id(state_id=state_id, db=db)
    if db_state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="state is Not found"
        )
    count = (
        db.query(CityModel.id)
        .filter(CityModel.state_id == state_id, CityModel.is_deleted == False)
        .count()
    )
    if count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="State has city"
        )
    db_state.is_deleted = True
    db_state.updated_at = now()
    db.commit()
    db.refresh(db_state)
    return f"{db_state.name} is deleted successfully"
