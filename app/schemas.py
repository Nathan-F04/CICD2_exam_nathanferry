from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict
from annotated_types import Ge, Le

NameStr = Annotated[str, StringConstraints(min_length=1, max_length=100)]
YearInt = Annotated[int, Ge(1900), Le(2100)]
TitleInt = Annotated[int, Ge(1), Le(255)]
PagesInt = Annotated[int, Ge(1), Le(10000)]
class AuthorCreate(BaseModel):
    name: NameStr
    email: EmailStr
    year_started: YearInt

class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    name: NameStr
    email: EmailStr
    year_started: YearInt

class AuthorPut(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    name: NameStr
    email: EmailStr
    year_started: YearInt

class AuthorPartialUpdate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    name: Optional[NameStr] = None
    email: Optional[EmailStr] = None
    year_started: Optional[YearInt] = None

class BookCreate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    title: TitleInt
    pages:PagesInt

class BookRead(BaseModel):
    id: int
    title: TitleInt
    pages: PagesInt
    author_id: int