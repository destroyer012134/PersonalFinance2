# Crear un usuario
from fastapi import HTTPException
from appv1.schemas.user import UserCreate, UserUpdate
from core.security import get_hashed_password
from core.utils import generate_user_id
from sqlalchemy.orm import Session
from sqlalchemy import false, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# Consultar un usuario por su ID
def get_user_by_id(db: Session, user_id: str):
    sql = text("SELECT * FROM users WHERE user_id = :user_id")
    result = db.execute(sql, {"user_id": user_id}).fetchone()
    return result




def create_user_sql(db: Session, user: UserCreate):
    try:
        sql_query = text(
        "INSERT INTO users (user_id, full_name, mail, passhash, user_role) "
        "VALUES (:user_id, :full_name, :mail, :passhash, :user_role)"
        )

    
        params = {
            "user_id": generate_user_id(),
            "full_name": user.full_name,
            "mail": user.mail,
            "passhash":get_hashed_password(user.passhash),
            "user_role": user.user_role,
        }
        db.execute(sql_query, params)
        db.commit()
        return True  # Retorna True si la inserción fue exitosa
    
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear usuario: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El ID generado automaticamente ya existe. Volver a intentar")
            if 'for key \'mail\'' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El email ya está registrado")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear usuario")
    except SQLAlchemyError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al crear usuario")
    


    # Consultar un usuario por su email
def get_user_by_email(db: Session, p_mail: str):
        try:
             sql = text("SELECT * FROM users WHERE mail = :mail")
             result = db.execute(sql, {"mail": p_mail}).fetchone()
             #  solo busca uno como el limit 1
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar usuario por email: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar usuario por email")


   # Consultar todos los usuarios
def get_all_users(db: Session):
        try:
             sql = text("SELECT * FROM users WHERE user_status = true")
             result = db.execute(sql).fetchall()
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar usuario: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar usuario")
        


        
           # Consultar un usuario por su role
def get_users_by_role(db: Session, role: str):
        try:
             sql = text("SELECT * FROM users WHERE user_role = :user_role")
             result = db.execute(sql, {"user_role": role}).fetchall()
             return result
        
        except SQLAlchemyError as e:
            print(f"Error al buscar usuario por role: {e}")
            raise HTTPException(status_code=500, detail="Error al buscar usuario por role")



def update_user(db: Session, user_id: str, user: UserUpdate): 
    try:
        sql = "UPDATE users SET "
        params = {"user_id": user_id}
        updates = []
        if user.full_name:
            updates.append("full_name = :full_name")
            params["full_name"] = user.full_name
        if user.mail:
            updates.append("mail = :mail")
            params["mail"] = user.mail
        if user.user_role:
            updates.append("user_role = :user_role")
            params["user_role"] = user.user_role
        if user.user_status is not None:
            updates.append("user_status = :user_status")
            params["user_status"] = user.user_status
        sql += ", ".join(updates) + " WHERE user_id = :user_id"         
        # Envuelve la consulta SQL en text()
        sql = text(sql)
        
        db.execute(sql, params)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al actualizar usuario: {e}")
        if 'for key \'mail\'' in str(e.orig):
            raise HTTPException(status_code=400, detail="Error. El email ya está registrado")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al actualizar usuario")
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")




def get_all_users_paginated(db: Session, page: int = 1, page_size: int = 10):
    try:
        # Calcular el offset basado en el número de página y el tamaño de página
        offset = (page - 1) * page_size

        # Consulta SQL con paginación, incluyendo todos los campos requeridos
        sql = text(
            "SELECT user_id, full_name, mail, user_role, user_status, created_at, updated_at "
            "FROM users "
            "ORDER BY created_at DESC "  # Cambia esto por tu criterio de ordenación
            "LIMIT :page_size OFFSET :offset"
        )
        params = {
            "page_size": page_size,
            "offset": offset
        }
        result = db.execute(sql, params).mappings().all()

        # Obtener el número total de usuarios
        count_sql = text("SELECT COUNT(*) FROM users")
        total_users = db.execute(count_sql).scalar()

        # Calcular el número total de páginas
        total_pages = (total_users + page_size - 1) // page_size

        return result, total_pages
    except SQLAlchemyError as e:
        print(f"Error al obtener todos los usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener todos los usuarios")
    

    # Eliminar un usuario
def delete_user(db: Session, user_id: str, user: UserUpdate):
    try:
        sql = "UPDATE users SET "
        params = {"user_id": user_id}
        updates = []
        if user.user_status is not None:
            updates.append("user_status = :user_status")
            user.user_status = false
            params["user_status"] = user.user_status
        sql += ", ".join(updates) + " WHERE user_id = :user_id"         
        # Envuelve la consulta SQL en text()
        sql = text(sql)
        
        db.execute(sql, params)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
        print(f"Error al actualizar usuario: {e}")
        if 'for key \'mail\'' in str(e.orig):
            raise HTTPException(status_code=400, detail="Error. El email ya está registrado")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al actualizar usuario")
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")


    # try:
    #     sql = text("UPDATE FROM users WHERE user_id = :user_id")
    #     db.execute(sql, {"user_id": user_id})
    #     db.commit()
    #     return True
    # except IntegrityError as e:
    #     db.rollback()  # Revertir la transacción en caso de error de integridad (llave foránea)
    #     print(f"Error al eliminar usuario: {e}")
    #     raise HTTPException(status_code=400, detail="Error. Integridad de datos al eliminar usuario")
    # except SQLAlchemyError as e:
    #     db.rollback()  
    #     print(f"Error al eliminar usuario: {e}")
    #     raise HTTPException(status_code=500, detail="Error al eliminar usuario")