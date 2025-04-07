import os
from .models.users import User, UserRoleEnum
from .config.db import db
from .config.jwt_hash import verify_password
from sqlalchemy import or_
from .models import UserAdmin, UserRefreshTokenAdmin
from .models import CharacterAdmin, CharacterImageAdmin
from .models import CreatureAdmin, CreatureImageAdmin
from .models import DroidAdmin, DroidImageAdmin
from .models import LocationAdmin, LocationImageAdmin, TerrainAdmin, LocationTerrainAdmin
from .models import OrganizationAdmin, OrganizationImageAdmin
from .models import SpecieAdmin, SpecieImageAdmin
from .models import VehicleAdmin, VehicleImageAdmin, VehicleLengthAdmin
from .models import WeaponAndTechAdmin, WeaponAndTechImageAdmin
from .models import MoreAdmin, MoreImageAdmin


def init(admin_backend):
    admin_backend.add_view(UserAdmin)
    admin_backend.add_view(UserRefreshTokenAdmin)

    admin_backend.add_view(CharacterAdmin)
    admin_backend.add_view(CharacterImageAdmin)

    admin_backend.add_view(CreatureAdmin)
    admin_backend.add_view(CreatureImageAdmin)

    admin_backend.add_view(DroidAdmin)
    admin_backend.add_view(DroidImageAdmin)

    admin_backend.add_view(LocationAdmin)
    admin_backend.add_view(LocationImageAdmin)
    admin_backend.add_view(TerrainAdmin)
    admin_backend.add_view(LocationTerrainAdmin)

    admin_backend.add_view(OrganizationAdmin)
    admin_backend.add_view(OrganizationImageAdmin)

    admin_backend.add_view(SpecieAdmin)
    admin_backend.add_view(SpecieImageAdmin)

    admin_backend.add_view(VehicleAdmin)
    admin_backend.add_view(VehicleImageAdmin)
    admin_backend.add_view(VehicleLengthAdmin)

    admin_backend.add_view(WeaponAndTechAdmin)
    admin_backend.add_view(WeaponAndTechImageAdmin)

    admin_backend.add_view(MoreAdmin)
    admin_backend.add_view(MoreImageAdmin)
    

def authenticate(username: str, password: str) -> bool:
    user = db.query(User).filter(or_(User.username == username, User.email == username)).first()
    if user:
        if user.role == UserRoleEnum.ADMIN:
            return verify_password(password, user.password)
    return False