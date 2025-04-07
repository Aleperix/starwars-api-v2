from ..config.db import Base
from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Vehicle(BaseStarWars):
    __tablename__ = "vehicles"

    width = Column(String(64), unique=False, nullable=True)
    height = Column(String(64), unique=False, nullable=True)
    diameter = Column(String(64), unique=False, nullable=True)
    length = relationship('VehicleLength', back_populates='vehicle')
    image = relationship('VehicleImage', back_populates='vehicle', uselist=False)
    

    def __repr__(self):
        return f'<Vehicle {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "width": self.width,
            "height": self.height,
            "diameter": self.diameter,
            "length": [length.serialize() for length in self.length],
            "image": self.image.serialize() if self.image else None
        }
class VehicleAdmin(ModelView, model=Vehicle):
    form_columns = ['name', 'slug', 'description', 'short_description', 'width', 'height', 'length', 'diameter', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-ship"
    category = "Vehicles"
    
class VehicleImage(BaseStarWarsImage):
    __tablename__ = "vehicle_images"

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship('Vehicle', back_populates='image')

    def __repr__(self):
        return f'<VehicleImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class VehicleImageAdmin(BaseStarWarsImageAdmin, model=VehicleImage):
    category = "Vehicles"

class VehicleLength(Base):
    __tablename__ = "vehicle_length"

    id = Column(Integer, primary_key=True)
    length = Column(String(64), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship('Vehicle')

    def __repr__(self):
        return f'<VehicleLength {self.id}>'

    def serialize(self):
        return self.length
class VehicleLengthAdmin(ModelView, model=VehicleLength):
    form_columns = ['vehicle','length']
    column_list = ["id"] + form_columns
    icon="fa-solid fa-ruler-horizontal"
    category = "Vehicles"