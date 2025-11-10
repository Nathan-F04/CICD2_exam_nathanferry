# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base
from app.schemas import AuthorCreate, AuthorRead, AuthorPut, AuthorPartialUpdate, BookCreate, BookRead
#from app.schemas import 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

def commit_or_rollback(db: Session, error_msg: str):
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=409, detail=error_msg)


@app.post("/api/authors", response_model = AuthorRead, status_code = 201)
def post_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    db_author = AuthorDB(**payload.model_dump())
    db.add(db_author)
    commit_or_rollback(db, "Author already exists")
    db.refresh(db_author)
    return db_author

@app.get("/api/authors", response_model=list[AuthorRead], status_code=200)
def list_authors(limit: int=10, offset:int=0, db: Session = Depends(get_db)):
    stmt = select(AuthorDB).orderby(AuthorDB.id).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()

@app.get("/api/authors/{id}", response_model=AuthorRead, status_code=200)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db,get(AuthorDB, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.put("/api/authors/{id}", response_model=AuthorRead, status_code=200)
def put_author(author_id: int, payload: AuthorPut, db: Session = Depends(get_db)):
    author = db.get(AuthorDB, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    edit = AuthorDB(**payload.model_dump())
    stmt = update(AuthorDB).where(AuthorDB.id == author_id).values(id = edit.id, name = edit.name, email = edit.email, year_started = edit.year_started)
    db.execute(stmt)
    commit_or_rollback(db, detail="Already exists")
    return edit

@app.patch("/api/authors/{id}", response_model=AuthorRead, status_code=200)
def patch_author(author_id: int, payload: AuthorPartialUpdate, db: Session = Depends(get_db)):
    author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    edit = payload.model_dump(exclude_unset = True)
    for key, value in edit.items():
        setattr(new_details, key, value)
    db.add(new_details)
    commit_or_rollback(db, detail="Already exists")
    db.refresh(new_details)
    return new_details


@app.delete("/api/authors/{id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(AuthorDB, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/api/books", response_model=BookRead, status_code=201)
def create_book(book: BookCreate, db:Session = Depends(get_db)):
    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    commit_or_rollback(db,"Book already exists")
    db.refresh(db_book)
    return db_book

@app.get("/api/books", response_model=list[BookRead], status_code=200)
def list_books(limit: int=10, offset:int=0, db:Session = Depends(get_db)):
    stmt = select(BookDB).orderby(BookDB.id).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()

@app.get("/api/books{id}", response_model=BookRead, status_code=200)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if not book:
        raise HTTPException(status_code = 404, detail = "book not found")
    
