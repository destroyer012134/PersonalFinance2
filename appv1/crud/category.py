# Crear un usuario

from fastapi import HTTPException
from appv1.schemas.category import CategoryCreate
from core.utils import generate_category_id
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def create_category_sql(db: Session, category: CategoryCreate):
    try:
        sql_query = text(
            "INSERT INTO category ( category_id, category_name, category_description"
            "VALUES (:category_id, :category_name, :category_description)"
        )

    
        params = {
            "category_id": generate_category_id(),
            "category_name": category.category_name,
            "category_description": category.category_description,
       
        }
        db.execute(sql_query, params)
        db.commit()
        return True
    

    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear categoria: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El ID generado automaticamente ya existe. Volver a intentar")
            
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear categoria")
    except SQLAlchemyError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear categoria: {e}")
        raise HTTPException(status_code=500, detail="Error al crear categoria")
    


 # Consultar un categoria por su nombre
def get_category_by_name(db: Session, name: str):
        try:
             sql = text("SELECT * FROM category WHERE name = :name")
             result = db.execute(sql, {"name": name}).fetchone()
             #  solo busca uno como el limit 1
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar categoria por nombre: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar categoria por nombre")




   # Consultar todos las categorias
def get_all_categories(db: Session):
        try:
             sql = text("SELECT * FROM catogory WHERE category_status = true")
             result = db.execute(sql).fetchall()
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar categorias: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar categorias")

      