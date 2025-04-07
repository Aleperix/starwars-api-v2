from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class More(BaseStarWars):
    __tablename__ = "mores"

    image = relationship('MoreImage', back_populates='more', uselist=False)

    def __repr__(self):
        return f'<More {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "image": self.image.serialize() if self.image else None
        }
class MoreAdmin(ModelView, model=More):
    form_columns = ['name', 'slug', 'description', 'short_description', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-ellipsis"
    category = "Mores"
    
class MoreImage(BaseStarWarsImage):
    __tablename__ = "more_images"

    more_id = Column(Integer, ForeignKey("mores.id"))
    more = relationship('More', back_populates='image')

    def __repr__(self):
        return f'<MoreImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class MoreImageAdmin(BaseStarWarsImageAdmin, model=MoreImage):
    category = "Mores"