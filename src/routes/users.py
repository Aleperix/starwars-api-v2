from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..config.db import db
from ..models import User, UserRefreshToken
from ..schemas.users import ANLogin, UserIn, UserOut
from ..config.jwt_hash import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, create_access_token, create_refresh_token, get_current_user_is_active, get_password_hash, login_user_is_active, token_is_valid, verify_password
from jose import JWTError, jwt
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

users_router = APIRouter(prefix="/api/users", tags=["users"])

#Create one user
@users_router.post("", response_model=UserOut, include_in_schema=False)
def create_user(user: UserIn):
    hashed_pwd = get_password_hash(user.password)
    new_user = User(username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email, password=hashed_pwd, is_active=user.is_active | False)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user.serialize()
    except IntegrityError as error:
        db.rollback()  # Deshacer la transacción en caso de error
        print(error.orig)
        print(str(error.orig).split(")=(")[0].split("(")[1])
        unique_column = str(error.orig).split(")=(")[0].split("(")[1]
        if unique_column == "username" or "email":
            raise HTTPException(status_code=404, detail=f"The {unique_column} is already in use.")
    
    

#Login user
@users_router.post("/login", response_model=ANLogin, include_in_schema=False)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    device_id = request.headers.get("X-Device-ID", "") if request.headers.get("X-Device-ID") else None
    ip_address = request.client.host if request.client else None
    if not device_id or not ip_address:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(User).filter(or_(User.username == form_data.username, User.email == form_data.username)).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User {form_data.username} not found.")
    login_user_is_active(db_user.serialize()["is_active"])
    user = verify_password(form_data.password, db_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": form_data.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": form_data.username})

    # 🔹 Guardar el nuevo refresh token en la BD usando la relación
    refresh_token_entry = UserRefreshToken(token=refresh_token, user=db_user, device_id=device_id, ip_address=ip_address)
    db.add(refresh_token_entry)
    db.commit()

    # Establecer el refresh token en una cookie httpOnly
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer", "user": db_user.serialize()}
)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 7 días
        secure=False,  # Si usas HTTPS
        samesite=None
    )
    return response



@users_router.post("/refresh", response_model=dict, include_in_schema=False)
def refresh_token(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        device_id = request.headers.get("X-Device-ID") if request.headers.get("X-Device-ID") else None
        ip_address = request.client.host if request.client else None  # Obtener la IP pública del usuario

        if not refresh_token or not device_id or not ip_address:
            raise HTTPException(status_code=401, detail="Invalid token")
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # 🔹 Buscar el refresh token usando la relación en lugar de hacer otra query
        if not user.refresh_tokens.filter(UserRefreshToken.token == refresh_token, UserRefreshToken.device_id == device_id, UserRefreshToken.ip_address == ip_address).first():
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        return {"access_token": new_access_token, "token_type": "bearer", "user": user.serialize()}	

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#Logout current logged user
@users_router.post("/logout", include_in_schema=False)
def logout(request: Request, current_user: dict = Depends(token_is_valid)):
    user = current_user["user"]
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found.")
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 🔹 Intentar eliminar el token y verificar cuántos registros se eliminaron
    deleted_count = user.refresh_tokens.filter(UserRefreshToken.token == refresh_token).delete()
    db.commit()

    if deleted_count == 0:  # Si no se eliminó ningún token, significa que no existía
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": "Logged out successfully"}

#Verify current user is auth
@users_router.get("/isauth", response_model=UserOut, include_in_schema=False)
async def is_auth(current_user: UserOut = Depends(get_current_user_is_active)):
    return current_user["user"].serialize()