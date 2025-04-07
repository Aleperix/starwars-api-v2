from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.routes.users import users_router
from src.routes.starwars import characters_router, creatures_router, droids_router, locations_router, organizations_router, species_router, vehicles_router, weapon_and_techs_router, more_router
from src.config.db import engine, Base
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
import src.admin as admin_backend

app = FastAPI(
    title="StarWars Data API", #Docs page project title
    description="A FastAPI backend of StarWars Data", #Docs page project description
    version="1.0", #Docs page project version
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} #Remove schemas from docs page
)

# Clase de autenticación personalizada para SQLAdmin
class CustomAuth(AuthenticationBackend):
    async def authenticate(self, request: Request) -> bool:
        return "user" in request.session
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if admin_backend.authenticate(username, password):
            request.session["user"] = username
            return True
        return False

    async def logout(self, request: Request):
        request.session.clear()

admin = Admin(app, engine, authentication_backend=CustomAuth(secret_key="your_secret_key"))
admin_backend.init(admin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",include_in_schema=False)
def index():
    return {"message": "Working"}


app.include_router(users_router)
app.include_router(characters_router)
app.include_router(creatures_router)
app.include_router(droids_router)
app.include_router(locations_router)
app.include_router(organizations_router)
app.include_router(species_router)
app.include_router(vehicles_router)
app.include_router(weapon_and_techs_router)
app.include_router(more_router)



Base.metadata.create_all(engine)

if __name__=="__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)