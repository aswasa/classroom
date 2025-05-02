from fastapi import APIRouter
from database.teacherservice import *
from typing import Optional
from auth_config import config, security
from fastapi import Response, Depends, Request

teacher_side = APIRouter(prefix="/teacher", tags=["Учительская часть"])

@teacher_side.post("/register", summary="Регистрация")
async def add_teacher(user_name: str, phone_number: str, email: str, password: str, response: Response):
    result = register(user_name, phone_number, email, password)
    if result:
        token = security.create_access_token(uid=str(result))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"teacher_id": result} if result else {"error": "Ошибка регистрации"}

@teacher_side.post("/login", summary="Вход")
async def login_teacher(email: str, password: str, response: Response):
    token = login(email, password)
    if token:
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"message": "Вы вошли в аккаунт",  "access_token": token} if token else {"error": "Неверные данные"}

@teacher_side.post("/logout", summary="Выход")
async def logout_teacher(email: str, response: Response):
    success = logout(email)
    if success:
        response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из аккаунта"} if success else {"error": "Неверные данные"}

@teacher_side.delete("/delete_account", summary="Удалить аккаунт", dependencies=[Depends(security.access_token_required)])
async def remove_account(password: str, response: Response, request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    success = delete_account(teacher_id, password)
    if success:
        response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы удалили аккаунт"} if success else {"error": "Неверные данные"}

@teacher_side.post("/create_course", summary="Создать курс", dependencies=[Depends(security.access_token_required)])
async def create_new_course(name: str, request: Request, user_data=Depends(security.access_token_required), description: Optional[str] = None):
    teacher_id = int(user_data.uid)
    course_id = create_course(name, description, teacher_id)
    return {"message": f"Вы создали курс, его айди: {course_id}"} if course_id else {"error": "Неверные данные"}

@teacher_side.delete("/delete_course", summary="Удалить курс", dependencies=[Depends(security.access_token_required)])
async def remove_course(name: str, request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    success = delete_course(name, teacher_id)
    return {"message": "Курс успешно удален"} if success else {"error": "Неверные данные"}

@teacher_side.post("/add_hw", summary="Добавить домашнее задание", dependencies=[Depends(security.access_token_required)])
async def add_homework(title: str, text: str, deadline: str, max_mark: int, request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    hw_id = add_hw(teacher_id, title, text, deadline, max_mark)
    return {"message": f"Вы добавили домашнее задание, его айди: {hw_id}"} if hw_id else {"error": "Неверные данные"}

@teacher_side.delete("/delete_hw", summary="Удалить домашнее задание", dependencies=[Depends(security.access_token_required)])
async def remove_homework(title: str, request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    success = delete_hw(title,teacher_id)
    return {"message": "Вы удалили домашнее задание"} if success else {"error": "Неверные данные"}

@teacher_side.put("/redact_hw", summary="Редактировать домашнее задание", dependencies=[Depends(security.access_token_required)])
async def update_homework(title: str, new_text: str, new_deadline: str, request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    success = redact_hw(title, new_text, new_deadline, teacher_id)
    return {"message": "Вы обновили домашнее задание"} if success else {"error": "Неверные данные"}

@teacher_side.post("/check_hw", summary="Проверить домашнее задание", dependencies=[Depends(security.access_token_required)])
async def grade_homework(hw_id: int, mark: int, user_id: int, request: Request, user_data=Depends(security.access_token_required), feedback: Optional[str] = None):
    teacher_id = int(user_data.uid)
    mark_id = check_hw(hw_id, mark, user_id, teacher_id, feedback)
    return {"message": "Вы оценили домашнее задание"} if mark_id else {"error": "Неверные данные"}

@teacher_side.get("/profile", summary="Профиль", dependencies=[Depends(security.access_token_required)])
async def get_profile(request: Request, user_data=Depends(security.access_token_required)):
    teacher_id = int(user_data.uid)
    profile = profile_teacher(teacher_id)
    return {"message": f"Профиль учителя {profile}"} if profile else {"error": "Неверные данные"}
