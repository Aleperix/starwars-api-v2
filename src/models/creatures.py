from .starwars import BaseStarWars, BaseStarWarsImage, GenderEnum, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqladmin import ModelView
   
class Creature(BaseStarWars):
    __tablename__ = "creatures"

    gender = Column(Enum(GenderEnum), unique=False, nullable=False)
    height = Column(String(50), unique=False, nullable=True)
    length = Column(String(50), unique=False, nullable=True)
    width = Column(String(50), unique=False, nullable=True)
    image = relationship('CreatureImage', back_populates='creature', uselist=False)

    def __repr__(self):
        return f'<Creature {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "gender": self.gender.value,
            "height": self.height,
            "length": self.length,
            "width": self.width,
            "image": self.image.serialize() if self.image else None
        }
class CreatureAdmin(ModelView, model=Creature):
    icon="fa-solid fa-paw"
    category = "Creatures"
    form_columns = ['name', 'slug', 'description', 'short_description', 'gender', 'height', 'length', 'width', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns    
        
class CreatureImage(BaseStarWarsImage):
    __tablename__ = "creature_images"

    creature_id = Column(Integer, ForeignKey("creatures.id"))
    creature = relationship('Creature', back_populates='image')
    
    def __repr__(self):
        return f'<CreatureImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class CreatureImageAdmin(BaseStarWarsImageAdmin, model=CreatureImage):
    category = "Creatures"
