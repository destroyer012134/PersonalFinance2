# Crear un usuario
from fastapi import HTTPException
from appv1.schemas.user import UserCreate, UserUpdate
from core.security import get_hashed_password
from core.utils import generate_user_id
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


    # Consultar permisos de un rol por cada modulo
def get_permissions(db: Session, rol: str, module: str):
        try:
             sql = text("SELECT p_select, p_insert, p_update, p_delete FROM permissions WHERE rol_name = :rol AND module_name = :module ")
             result = db.execute(sql, {"rol": rol, "module": module}).fetchone()
             #  solo busca uno como el limit 1
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al obtener permisos: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar usuario por email")
