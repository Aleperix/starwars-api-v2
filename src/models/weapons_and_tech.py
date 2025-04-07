from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class WeaponAndTech(BaseStarWars):
    __tablename__ = "weapons_and_techs"    
    
    length = Column(String(64), unique=False, nullable=True)
    diameter = Column(String(64), unique=False, nullable=True)
    image = relationship('WeaponAndTechImage', back_populates='weapon_and_tech', uselist=False)
    

    def __repr__(self):
        return f'<WeaponAndTech {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "length": self.length,
            "diameter": self.diameter,
            "image": self.image.serialize() if self.image else None
        }
class WeaponAndTechAdmin(ModelView, model=WeaponAndTech):
    form_columns = ['name', 'slug', 'description', 'short_description', 'length', 'diameter', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-gun"
    category = "WeaponsAndTechs"
    
    
class WeaponAndTechImage(BaseStarWarsImage):
    __tablename__ = "weapons_and_tech_images"

    weapon_and_tech_id = Column(Integer, ForeignKey("weapons_and_techs.id"))
    weapon_and_tech = relationship('WeaponAndTech', back_populates='image')

    def __repr__(self):
        return f'<WeaponAndTechImage {self.id}>'
    
    def serialize(self):
        return super().serialize_data()
class WeaponAndTechImageAdmin(BaseStarWarsImageAdmin, model=WeaponAndTechImage):
    category = "WeaponsAndTechs"
    