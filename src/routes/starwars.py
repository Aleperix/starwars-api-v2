import os, math
from fastapi import APIRouter, HTTPException
from ..schemas.starwars import CharacterResponse, CharactersResponse
from ..schemas.starwars import CreatureResponse, CreaturesResponse
from ..schemas.starwars import DroidResponse, DroidsResponse
from ..schemas.starwars import LocationResponse, LocationsResponse
from ..schemas.starwars import OrganizationResponse, OrganizationsResponse
from ..schemas.starwars import SpecieResponse, SpeciesResponse
from ..schemas.starwars import VehicleResponse, VehiclesResponse
from ..schemas.starwars import WeaponAndTechResponse, WeaponAndTechsResponse
from ..schemas.starwars import MoreResponse, MoresResponse
from ..config.db import db
from ..models import Character, Creature, Droid, Location, Organization, Specie, Vehicle, WeaponAndTech, More

characters_router = APIRouter(prefix="/api/characters", tags=["characters"])
creatures_router = APIRouter(prefix="/api/creatures", tags=["creatures"])
droids_router = APIRouter(prefix="/api/droids", tags=["droids"])
locations_router = APIRouter(prefix="/api/locations", tags=["locations"])
organizations_router = APIRouter(prefix="/api/organizations", tags=["organizations"])
species_router = APIRouter(prefix="/api/species", tags=["species"])
vehicles_router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])
weapon_and_techs_router = APIRouter(prefix="/api/weapon_and_techs", tags=["weapon_and_techs"])
more_router = APIRouter(prefix="/api/more", tags=["more"])

LIST_RESPONSE_LIMIT = int(os.environ.get("LIST_RESPONSE_LIMIT", 10))


def get_objects(model, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    count = db.query(model).count()
    total_pages = math.ceil(count / limit)
    if page < 1 or page > total_pages:
        raise HTTPException(status_code=404, detail="Not found")
    objects = db.query(model).offset(offset).limit(limit).all()
    if len(objects) < 1:
        raise HTTPException(status_code=404, detail="Not found")
    objects = [object.serialize() for object in objects]
    return {
        f"{model.__tablename__}": objects,
        "page": page,
        "total_pages": total_pages,
        "count": count,
        "limit": limit,
        "next": f"/api/{model.__tablename__}?page={page + 1}" if page < total_pages else None,
        "previous": f"/api/{model.__tablename__}?page={page - 1}" if page > 1 else None
    }

def get_object(model, id: int):
    count = db.query(model).count()
    object = db.query(model).get(id)
    if not object:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        f"{model.__tablename__[:-1] if model.__tablename__[-1] == 's' else model.__tablename__}": object.serialize(),
        "count": count,
        "next": object.id + 1 if object.id < count else None,
        "previous": object.id - 1 if object.id > 1 else None
    }

@characters_router.get("", response_model=CharactersResponse)
def get_all_characters(page: int = 1):
    return get_objects(Character, page, LIST_RESPONSE_LIMIT)

@characters_router.get("/{id}", response_model=CharacterResponse)
def get_one_character(id: int):
    return get_object(Character, id)

@creatures_router.get("", response_model=CreaturesResponse)
def get_all_creatures(page: int = 1):
    return get_objects(Creature, page, LIST_RESPONSE_LIMIT)

@creatures_router.get("/{id}", response_model=CreatureResponse)
def get_one_creature(id: int):
    return get_object(Creature, id)

@droids_router.get("", response_model=DroidsResponse)
def get_all_droids(page: int = 1):
    return get_objects(Droid, page, LIST_RESPONSE_LIMIT)

@droids_router.get("/{id}", response_model=DroidResponse)
def get_one_droid(id: int):
    return get_object(Droid, id)

@locations_router.get("", response_model=LocationsResponse)
def get_all_locations(page: int = 1):
    return get_objects(Location, page, LIST_RESPONSE_LIMIT)

@locations_router.get("/{id}", response_model=LocationResponse)
def get_one_location(id: int):
    return get_object(Location, id)

@organizations_router.get("", response_model=OrganizationsResponse)
def get_all_organizations(page: int = 1):
    return get_objects(Organization, page, LIST_RESPONSE_LIMIT)

@organizations_router.get("/{id}", response_model=OrganizationResponse)
def get_one_organization(id: int):
    return get_object(Organization, id)

@species_router.get("", response_model=SpeciesResponse)
def get_all_species(page: int = 1):
    return get_objects(Specie, page, LIST_RESPONSE_LIMIT)

@species_router.get("/{id}", response_model=SpecieResponse)
def get_one_specie(id: int):
    return get_object(Specie, id)

@vehicles_router.get("", response_model=VehiclesResponse)
def get_all_vehicles(page: int = 1):
    return get_objects(Vehicle, page, LIST_RESPONSE_LIMIT)

@vehicles_router.get("/{id}", response_model=VehicleResponse)
def get_one_vehicle(id: int):
    return get_object(Vehicle, id)

@weapon_and_techs_router.get("", response_model=WeaponAndTechsResponse)
def get_all_weapon_and_techs(page: int = 1):
    return get_objects(WeaponAndTech, page, LIST_RESPONSE_LIMIT)

@weapon_and_techs_router.get("/{id}", response_model=WeaponAndTechResponse)
def get_one_weapon_and_tech(id: int):
    return get_object(WeaponAndTech, id)

@more_router.get("", response_model=MoresResponse)
def get_all_mores(page: int = 1):
    return get_objects(More, page, LIST_RESPONSE_LIMIT)

@more_router.get("/{id}", response_model=MoreResponse)
def get_one_more(id: int):
    return get_object(More, id)
    

