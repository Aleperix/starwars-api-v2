from pydantic import BaseModel, ConfigDict
from typing import Optional, Union

class Image(BaseModel):
    ratio_1x1: str
    ratio_2x1: str
    ratio_4x3: str
    ratio_16x9: str

class BaseObjectResponse(BaseModel):
    count: int
    next: Optional[Union[str, int]] = None
    previous: Optional[Union[str, int]] = None
    


class BaseObject(BaseModel):
    name: str
    slug: str
    description: str
    short_description: str
    image: Optional[Image] = None

class ObjectsResponse(BaseObjectResponse):
    page: int
    total_pages: int
    limit: int

class BaseCharacter(BaseObject):
    gender: Optional[str] = None
    height: Optional[str] = None
    length: Optional[str] = None

class CharacterIn(BaseCharacter):
    pass

class CharacterOut(BaseCharacter):
    id: int

class CharacterResponse(BaseObjectResponse):
    character: CharacterOut

class CharactersResponse(ObjectsResponse):
    characters: list[CharacterOut]

class BaseCreature(BaseObject):
    gender: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    length: Optional[str] = None

class CreatureIn(BaseCreature):
    pass

class CreatureOut(BaseCreature):
    id: int

class CreatureResponse(BaseObjectResponse):
    creature: CreatureOut

class CreaturesResponse(ObjectsResponse):
    creatures: list[CreatureOut]

class BaseDroid(BaseObject):
    height: Optional[str] = None
    length: Optional[str] = None

class DroidIn(BaseDroid):
    pass

class DroidOut(BaseDroid):
    id: int

class DroidResponse(BaseObjectResponse):
    droid: DroidOut

class DroidsResponse(ObjectsResponse):
    droids: list[DroidOut]

class BaseLocation(BaseObject):
    climate: Optional[str] = None
    terrains: Optional[list[str]] = None

class LocationIn(BaseLocation):
    pass

class LocationOut(BaseLocation):
    id: int

class LocationResponse(BaseObjectResponse):
    location: LocationOut

class LocationsResponse(ObjectsResponse):
    locations: list[LocationOut]

class BaseOrganization(BaseObject):
    height: Optional[str] = None

class OrganizationIn(BaseOrganization):
    pass

class OrganizationOut(BaseOrganization):
    id: int

class OrganizationResponse(BaseObjectResponse):
    organization: OrganizationOut

class OrganizationsResponse(ObjectsResponse):
    organizations: list[OrganizationOut]

class BaseSpecie(BaseObject):
    height: Optional[str] = None

class SpecieIn(BaseSpecie):
    pass

class SpecieOut(BaseSpecie):
    id: int

class SpecieResponse(BaseObjectResponse):
    specie: SpecieOut

class SpeciesResponse(ObjectsResponse):
    species: list[SpecieOut]

class BaseVehicle(BaseObject):
    width: Optional[str] = None
    height: Optional[str] = None
    length: Optional[list[str]] = None
    diameter: Optional[str] = None

class VehicleIn(BaseVehicle):
    pass

class VehicleOut(BaseVehicle):
    id: int

class VehicleResponse(BaseObjectResponse):
    vehicle: VehicleOut

class VehiclesResponse(ObjectsResponse):
    vehicles: list[VehicleOut]

class BaseWeaponAndTech(BaseObject):
    length: Optional[str] = None
    diameter: Optional[str] = None

class WeaponAndTechIn(BaseWeaponAndTech):
    pass

class WeaponAndTechOut(BaseWeaponAndTech):
    id: int

class WeaponAndTechResponse(BaseObjectResponse):
    weapons_and_tech: WeaponAndTechOut

class WeaponAndTechsResponse(ObjectsResponse):
    weapons_and_techs: list[WeaponAndTechOut]

class BaseMore(BaseObject):
    pass

class MoreIn(BaseMore):
    pass

class MoreOut(BaseMore):
    id: int

class MoreResponse(BaseObjectResponse):
    more: MoreOut

class MoresResponse(ObjectsResponse):
    mores: list[MoreOut]
    