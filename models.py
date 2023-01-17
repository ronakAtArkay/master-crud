from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class SeaRegionModel(Base):
    __tablename__ = "sea_regions"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class CountryModel(Base):
    __tablename__ = "countrys"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    sea_region_id = Column(String(36), ForeignKey("sea_regions.id"))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    sea_region = relationship("SeaRegionModel", backref="countrys")


class StateModel(Base):
    __tablename__ = "states"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    country_id = Column(String(36), ForeignKey("countrys.id"))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    country = relationship("CountryModel", backref="states")


class CityModel(Base):
    __tablename__ = "citys"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    state_id = Column(String(36), ForeignKey("states.id"))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    state = relationship("StateModel", backref="citys")
