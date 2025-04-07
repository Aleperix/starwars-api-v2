from .starwars import BaseStarWars, BaseStarWarsImage, BaseStarWarsImageAdmin
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqladmin import ModelView

class Organization(BaseStarWars):
    __tablename__ = "organizations"

    height = Column(String(64), unique=False, nullable=True)
    image = relationship('OrganizationImage', back_populates='organization', uselist=False)

    def __repr__(self):
        return f'<Organization {self.name}>'

    def serialize(self):
        base_data = super().serialize_data()
        return {
            **base_data,
            "height": self.height,
            "image": self.image.serialize() if self.image else None
        }
class OrganizationAdmin(ModelView, model=Organization):
    form_columns = ['name', 'slug', 'description', 'short_description', 'height', 'is_active', 'image']
    column_details_list = form_columns
    column_list = ["id"] + form_columns
    icon="fa-solid fa-users"
    category = "Organizations" 
    
class OrganizationImage(BaseStarWarsImage):
    __tablename__ = "organization_images"

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship('Organization', back_populates='image')

    def __repr__(self):
        return f'<OrganizationImage {self.id}>'

    def serialize(self):
        return super().serialize_data()
class OrganizationImageAdmin(BaseStarWarsImageAdmin, model=OrganizationImage):
    category = "Organizations"
    