
#Generate more dynamic and hierarchy models
from ..config.db import Base
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqladmin import ModelView
import enum

class BaseStarWars(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    slug = Column(String(128), unique=True, nullable=False)
    description = Column(Text, unique=False, nullable=False)
    short_description = Column(Text, unique=False, nullable=False)
    is_active = Column(Boolean(), unique=False, nullable=False)

    def serialize_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "short_description": self.short_description,
            "is_active": self.is_active,
        }

class BaseStarWarsImage(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    ratio_1x1 = Column(String(256), nullable=False)
    ratio_2x1 = Column(String(256), nullable=False)
    ratio_4x3 = Column(String(256), nullable=False)
    ratio_16x9 = Column(String(256), nullable=False)

    def serialize_data(self):
        return {
            "ratio_1x1": self.ratio_1x1,
            "ratio_2x1": self.ratio_2x1,
            "ratio_4x3": self.ratio_4x3,
            "ratio_16x9": self.ratio_16x9
        }

class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    
from sqladmin import ModelView

class BaseStarWarsImageAdmin(ModelView):
    form_columns = ['ratio_1x1', 'ratio_2x1', "ratio_4x3", "ratio_16x9"]
    column_list = ["id"] + form_columns
    icon="fa-solid fa-image"

