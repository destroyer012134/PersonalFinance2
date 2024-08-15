# Crear un usuario

from appv1.schemas.role import RoleCreate
from fastapi import HTTPException
from core.utils import generate_category_id
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def create_role_sql(db: Session, role: RoleCreate):
    try:
        sql_query = text(
            "INSERT INTO roles ( rol_name"
            "VALUES (:rol_name)"
        )

    
        params = {
            "rol_name": role.rol_name,

        }
        db.execute(sql_query, params)
        db.commit()
        return True
    

    except IntegrityError as e:
        db.rollback()  
        print(f"Error al crear rol: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El Rol ya existe")
            
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear rol")
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"Error al crear rol: {e}")
        raise HTTPException(status_code=500, detail="Error al crear rol")
    


 # Consultar un categoria por su nombre
def get_role_by_name(db: Session, name: str):
        try:
             sql = text("SELECT * FROM roles WHERE role_name = :role_name")
             result = db.execute(sql, {"role_name": name}).fetchone()
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar rol por nombre: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar rol por nombre")


   # Consultar todos los roles
def get_all_roles(db: Session):
        try:
             sql = text("SELECT * FROM roles")
             result = db.execute(sql).fetchall()
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar roles: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar roles")


      