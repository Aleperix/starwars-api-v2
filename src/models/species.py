from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Specie(BaseStarWars):
    __tablename__ = "species"

    height = Column(String(50), unique=False, nullable=True)
    image = relationship('SpecieImage', back_populates='specie', uselist=False)

    def __repr__(self):
        return f'<Specie {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "height": self.height,
            "image": self.image.serialize() if self.image else None
        }
class SpecieAdmin(ModelView, model=Specie):
    form_columns = ['name', 'slug', 'description', 'short_description', 'height', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-dna"
    category = "Species"
    
    
class SpecieImage(BaseStarWarsImage):
    __tablename__ = "specie_images"

    specie_id = Column(Integer, ForeignKey("species.id"))
    specie = relationship('Specie', back_populates='image')

    def __repr__(self):
        return f'<SpecieImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class SpecieImageAdmin(BaseStarWarsImageAdmin, model=SpecieImage):
    category = "Species"