from typing import Annotated
from pydantic import BaseModel, StringConstraints
from datetime import datetime

class CategoryCreate(BaseModel):
    category_name: Annotated[str, StringConstraints(max_length=50)]
    category_description: Annotated[str, StringConstraints(max_length=120)]


class CategoryResponse(CategoryCreate):
    category_id: str
    category_status: bool = True
    created_at: datetime
    updated_at: datetime