from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

class AuthorCreate(BaseModel):
    name: NameStr
    email: EmailStr
    