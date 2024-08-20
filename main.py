from appv1.routers import category, login, role, users
from db.database import test_db_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(role.router, prefix="/role", tags=["role"])
app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(login.router, prefix="/login", tags=["logion"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)


@app.on_event("startup")
def on_startup():
    test_db_connection()

    
@app.get("/")
def read_root():
    return {
                "message": "ADSO 2670586",
                "autor": "Miguel Mor"
            }