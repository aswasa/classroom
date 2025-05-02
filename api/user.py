from fastapi import APIRouter
from database.userservice import *

user_side = APIRouter(prefix="/user", tags=["Пользовательская часть"])

@user_side.post("/register", summary="Регистрация")
async def add_user(user_name: str, phone_number: str, email: str, password: str):
    result = register(user_name, phone_number, email, password)
    return {"user_id": result} if result else {"error": "Ошибка регистрации"}

@user_side.post("/login", summary="Вход")
async def login_user(email: str, password: str):
    success = login(email, password)
    return {"message": "Вы вошли в аккаунт" } if success else {"error": "Неверные данные"}

@user_side.post("/logout", summary="Выход")
async def logout_user(email: str):
    success = logout(email)
    return {"message": "Вы вышли из аккаунта"} if success else {"error": "Неверные данные"}

@user_side.delete("/delete_account", summary="Удалить аккаунт")
async def remove_account(email: str, password: str):
    success = delete_account(email, password)
    return {"message": "Вы удалили аккаунт"} if success else {"error": "Неверные данные"}

# @user_side.post("/join_course", summary="Присоединиться к курсу")
# async def join_course(course_id: int, user_id: int):
#     success = choose_course(course_id, user_id)
#     return {"message": "Вы присоединились к курсу"} if success else {"error": "Неверные данные или вы уже состоите в этом курсе"}
#
# @user_side.post("/quit_course", summary="Покинуть курс")
# async def leave_course(user_id: int, course_id: int):
#     result = quit_course(user_id, course_id)
#     return {"message": "Вы вышли из курса"} if result else {"error": "Неверные данные"}
#
# @user_side.post("/submit_hw", summary="Отправить домашнее задание")
# async def submit_homework(user_id: int, hw_id: int, text: str, course_id: int, teacher_id: int):
#     result = add_hw(user_id, hw_id, text, course_id, teacher_id)
#     return {"message": "Вы сдали домашнее задание"} if result else {"error": "Неверные данные"}
#
# @user_side.delete("/delete_hw", summary="Удалить домашнее задание")
# async def remove_homework(hw_id: int, user_id: int):
#     success = delete_hw(hw_id, user_id)
#     return {"message": "Вы удалили домашнее задание"} if success else {"error": "Неверные данные"}

@user_side.post("/join_course", summary="Присоединиться к курсу")
async def join_course(course_id: int, user_id: int):
    success = choose_course(course_id, user_id)
    if success:
        return {"message": "Вы присоединились к курсу"}
    else:
        return {"error": "Неверные данные или вы уже состоите в этом курсе"}

@user_side.post("/quit_course", summary="Покинуть курс")
async def leave_course(user_id: int, course_id: int):
    result = quit_course(user_id, course_id)
    if result:
        return {"message": "Вы вышли из курса"}
    else:
        return {"error": "Неверные данные или вы не состоите в этом курсе"}

@user_side.post("/submit_hw", summary="Отправить домашнее задание")
async def submit_homework(user_id: int, hw_id: int, text: str, course_id: int, teacher_id: int):
    result = add_hw(user_id, hw_id, text, course_id, teacher_id)
    if result:
        return {"message": "Вы сдали домашнее задание"}
    else:
        return {"error": "Неверные данные или ошибка при добавлении задания"}

@user_side.delete("/delete_hw", summary="Удалить домашнее задание")
async def remove_homework(hw_id: int, user_id: int):
    success = delete_hw(hw_id, user_id)
    if success:
        return {"message": "Вы удалили домашнее задание"}
    else:
        return {"error": "Неверные данные или задание не найдено"}


@user_side.get("/profile", summary="Профиль")
async def get_profile(user_id: int):
    profile = profile_user(user_id)
    return {"message": f"Профиль ученика {profile}"} if profile else {"error": "Неверные данные"}
