from .. import models, schemas, oauth2
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix = "/tasks", tags = ["Tasks"])


# добавление задачи
@router.post("/", response_model = schemas.TaskResponse, summary = 'Написать задачу', status_code = status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Добавление задачи"""

    new_task = models.Task(user_id = user_id,**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# получение одной задачи
@router.get("/{id}", response_model = schemas.TaskResponse, summary = 'Посмотреть задачу с конкретным id')
def get_task(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Получить задачу по id"""

    task = db.query(models.Task).filter(models.Task.id == id).first()
    
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Задача с ID {id} не найдена"
        )
    
    if task.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You can not delete this task, you are not owner of it")


    return task

# получение всех задач
@router.get("/", response_model = list[schemas.TaskResponse], summary = 'Посмотреть задачи')
def get_all_tasks(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Получить список всех задач"""

    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    return tasks


# изменение статуса задачи
@router.patch("/{task_id}/description_status", response_model = schemas.TaskResponse, summary = 'Изменить статус задачи')
def change_task_status(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Изменение статус задачи"""

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Задача с ID {task_id} не найдена"
        )
    
    if task.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You can not patch this task, you are not owner of it")
    
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return task

# полностью меняем существующую задачу
@router.put("/{task_id}/status", response_model = schemas.TaskResponse, summary = 'Изменить задачу')
def change_all_task(task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Полное изменение задачи"""

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Задача с ID {task_id} не найдена"
        )
    
    if task.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You can not change this task, you are not owner of it")
    
    task.name = task_update.name
    task.description = task_update.description
    task.completed = task_update.completed

    db.commit()
    db.refresh(task)
    return task

# удаление задачи по ID
@router.delete("/{task_id}", summary = 'Удалить задачу', status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_validated_user_id)):
    """Удаление задачи по id"""

    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Задача с ID {task_id} не найдена"
        )
    
    if task.user_id != user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You can not delete this task, you are not owner of it")

    db.delete(task)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
