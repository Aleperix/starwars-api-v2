from .starwars import BaseStarWars, BaseStarWarsImage, GenderEnum, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Droid(BaseStarWars):
    __tablename__ = "droids"

    height = Column(String(50), unique=False, nullable=True)
    length = Column(String(50), unique=False, nullable=True)
    image = relationship('DroidImage', back_populates='droid', uselist=False)

    def __repr__(self):
        return f'<Droid {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "height": self.height,
            "length": self.length,
            "image": self.image.serialize() if self.image else None
        }
class DroidAdmin(ModelView, model=Droid):
    icon="fa-solid fa-robot"
    category = "Droids"
    form_columns = ['name', 'slug', 'description', 'short_description', 'height', 'length', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns

class DroidImage(BaseStarWarsImage):
    __tablename__ = "droid_images"

    droid_id = Column(Integer, ForeignKey("droids.id"))
    droid = relationship('Droid', back_populates='image')
    
    def __repr__(self):
        return f'<DroidImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class DroidImageAdmin(BaseStarWarsImageAdmin, model=DroidImage):
    category = "Droids"
    