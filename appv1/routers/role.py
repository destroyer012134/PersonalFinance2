from typing import List
from appv1.crud.role import create_role_sql, get_all_roles, get_role_by_name
from appv1.schemas.role import RoleCreate, RoleResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

@router.post("/create_role" )
async def insert_role(role: RoleCreate, db: Session = Depends(get_db)):
   respuesta = create_role_sql(db, role)

   if respuesta:
    return {"mensaje":"Rol registrado con exito"}
   

@router.get("/get-role-by-name/", response_model=RoleResponse)
async def read_category_by_name(name: str, db: Session = Depends(get_db)):
   role = get_role_by_name(db, name)
   if role is None:
      raise HTTPException(status_code=404, detail="role no encontrado")
   
   return role 

@router.get("/get-all-roles/", response_model=List[RoleResponse])
async def read_all_users( db: Session = Depends(get_db)):
   roles = get_all_roles(db)
   if len(roles)==0:
      raise HTTPException(status_code=404, detail="No hay roles ")
   
   return roles 

