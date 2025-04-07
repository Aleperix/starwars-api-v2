from .starwars import BaseStarWars, BaseStarWarsImage, GenderEnum, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Character(BaseStarWars):
    __tablename__ = "characters"

    gender = Column(Enum(GenderEnum), unique=False, nullable=False)
    height = Column(String(50), unique=False, nullable=True)
    length = Column(String(50), unique=False, nullable=True)
    image = relationship('CharacterImage', back_populates='character', uselist=False)

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "gender": self.gender.value,
            "height": self.height,
            "length": self.length,
            "image": self.image.serialize() if self.image else None
        }
        
        

class CharacterImage(BaseStarWarsImage):
    __tablename__ = "character_images"

    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship('Character', back_populates='image')
    
    def __repr__(self):
        return f'<CharacterImage {self.id}>'

    def serialize(self):
        return super().serialize_data()

class CharacterAdmin(ModelView, model=Character):
    icon="fa-solid fa-user"
    category = "Characters"
    form_columns = ['name', 'slug', 'description', 'short_description', 'gender', 'height', 'length', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns

class CharacterImageAdmin(BaseStarWarsImageAdmin, model=CharacterImage):
    category = "Characters"
    
    