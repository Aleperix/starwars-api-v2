from ..config.db import Base
from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Location(BaseStarWars):
    __tablename__ = "locations"

    climate = Column(String(64), unique=False, nullable=True)
    image = relationship('LocationImage', back_populates='location', uselist=False)
    location_terrains = relationship('LocationTerrain', back_populates='location')
    

    def __repr__(self):
        return f'<Location {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "climate": self.climate,	
            "image": self.image.serialize() if self.image else None,
            "terrains": [lt.terrain.serialize() for lt in self.location_terrains] if self.location_terrains else None
        }
class LocationAdmin(ModelView, model=Location):
    form_columns = ['name', 'slug', 'description', 'short_description', 'climate', 'terrains', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-globe"
    category = "Locations"

    
class LocationImage(BaseStarWarsImage):
    __tablename__ = "location_images"

    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship('Location', back_populates='image')

    def __repr__(self):
        return f'<LocationImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class LocationImageAdmin(BaseStarWarsImageAdmin, model=LocationImage):
    category = "Locations"

class Terrain(Base):
    __tablename__ = "terrains"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Terrain {self.name}>'
    
    def serialize(self):
        return self.name
class TerrainAdmin(ModelView, model=Terrain):
    form_columns = ['name']
    column_list = ["id"] + form_columns
    icon="fa-solid fa-mountain-sun"
    category = "Locations"
    

class LocationTerrain(Base):
    __tablename__ = "location_terrain"

    id = Column(Integer, primary_key=True)
    terrain_id = Column(Integer, ForeignKey("terrains.id"))
    terrain = relationship('Terrain')
    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship('Location')

    def __repr__(self):
        return f'<LocationTerrain {self.id}>'
    
    def serialize(self):
        return self.terrain.name,
class LocationTerrainAdmin(ModelView, model=LocationTerrain):
    form_columns = ['terrain', 'location']
    column_list = ["id"] + form_columns
    icon="fa-solid fa-link"
    category = "Locations"