from fastapi import APIRouter
from database.teacherservice import *
from typing import Optional

teacher_side = APIRouter(prefix="/teacher", tags=["Учительская часть"])

@teacher_side.post("/register", summary="Регистрация")
async def add_teacher(user_name: str, phone_number: str, email: str, password: str):
    result = register(user_name, phone_number, email, password)
    return {"teacher_id": result} if result else {"error": "Ошибка регистрации"}

@teacher_side.post("/login", summary="Вход")
async def login_teacher(email: str, password: str):
    success = login(email, password)
    return {"message": "Вы вошли в аккаунт" } if success else {"error": "Неверные данные"}

@teacher_side.post("/logout", summary="Выход")
async def logout_teacher(email: str):
    success = logout(email)
    return {"message": "Вы вышли из аккаунта"} if success else {"error": "Неверные данные"}

@teacher_side.delete("/delete_account", summary="Удалить аккаунт")
async def remove_account(email: str, password: str):
    success = delete_account(email, password)
    return {"message": "Вы удалили аккаунт"} if success else {"error": "Неверные данные"}

@teacher_side.post("/create_course", summary="Создать курс")
async def create_new_course(name: str, teacher_id: int, description: Optional[str] = None):
    course_id = create_course(name, description, teacher_id)
    return {"message": f"Вы создали курс, его айди: {course_id}"} if course_id else {"error": "Неверные данные"}

@teacher_side.delete("/delete_course", summary="Удалить курс")
async def remove_course(name: str, teacher_id: int):
    success = delete_course(name, teacher_id)
    return {"message": "Курс успешно удален"} if success else {"error": "Неверные данные"}

@teacher_side.post("/add_hw", summary="Добавить домашнее задание")
async def add_homework(teacher_id: int, title: str, text: str, deadline: str, max_mark: int):
    hw_id = add_hw(teacher_id, title, text, deadline, max_mark)
    return {"message": f"Вы добавили домашнее задание, его айди: {hw_id}"} if hw_id else {"error": "Неверные данные"}

@teacher_side.delete("/delete_hw", summary="Удалить домашнее задание")
async def remove_homework(title: str, teacher_id: int):
    success = delete_hw(title,teacher_id)
    return {"message": "Вы удалили домашнее задание"} if success else {"error": "Неверные данные"}

@teacher_side.put("/redact_hw", summary="Редактировать домашнее задание")
async def update_homework(title: str, new_text: str, new_deadline: str):
    success = redact_hw(title, new_text, new_deadline)
    return {"message": "Вы обновили домашнее задание"} if success else {"error": "Неверные данные"}

@teacher_side.post("/check_hw", summary="Проверить домашнее задание")
async def grade_homework(hw_id: int, mark: int, user_id: int, teacher_id: int, feedback: Optional[str] = None):
    mark_id = check_hw(hw_id, mark, user_id, teacher_id, feedback)
    return {"message": "Вы оценили домашнее задание"} if mark_id else {"error": "Неверные данные"}

@teacher_side.get("/profile", summary="Профиль")
async def get_profile(teacher_id: int):
    profile = profile_teacher(teacher_id)
    return {"message": f"Профиль учителя {profile}"} if profile else {"error": "Неверные данные"}
