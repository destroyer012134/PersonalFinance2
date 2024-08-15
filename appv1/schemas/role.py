from typing import Annotated
from pydantic import BaseModel, StringConstraints
from datetime import datetime

class RoleCreate(BaseModel):
    rol_name: Annotated[str, StringConstraints(max_length=15)]


class RoleResponse(RoleCreate):
    rol_name: str
    created_at: datetime
    updated_at: datetime