from .. import models, schemas, utils
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db

router = APIRouter(prefix = "/users", tags = ["Users"])

@router.post("/", response_model = schemas.UserOut ,summary = 'Добавить пользователя', status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #хэшируем пароль
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    try:
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Пользователь с таким email уже существует") 

@router.get("/{id}", response_model = schemas.UserOut, summary = 'Получить пользователя')
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
    
    return user