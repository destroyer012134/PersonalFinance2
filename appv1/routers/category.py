from typing import List
from fastapi import APIRouter, Depends, HTTPException
from appv1.crud.category import create_category_sql, get_all_categories, get_category_by_name
from appv1.schemas.category import CategoryCreate, CategoryResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import get_db

router = APIRouter()

@router.post("/create_category" )
async def insert_category(category: CategoryCreate, db: Session = Depends(get_db)):
   respuesta = create_category_sql(db, category)

   if respuesta:
    return {"mensaje":"Categoria registrada con exito"}
   

@router.get("/get-category-by-name/", response_model=CategoryResponse)
async def read_category_by_name(name: str, db: Session = Depends(get_db)):
   categoria = get_category_by_name(db, name)
   if categoria is None:
      raise HTTPException(status_code=404, detail="categoria no encontrada")
   
   return categoria 

@router.get("/get-all-categories/", response_model=List[CategoryResponse])
async def read_all_users( db: Session = Depends(get_db)):
   categorias = get_all_categories(db)
   if len(categorias)==0:
      raise HTTPException(status_code=404, detail="No hay categorias ")
   
   return categorias 

