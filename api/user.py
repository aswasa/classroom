from fastapi import APIRouter
from database.userservice import *
from auth_config import config, security
from fastapi import Response, Depends, Request

user_side = APIRouter(prefix="/user", tags=["Пользовательская часть"])

@user_side.post("/register", summary="Регистрация")
async def add_user(user_name: str, phone_number: str, email: str, password: str, response: Response):
    result = register(user_name, phone_number, email, password)
    if result:
        token = security.create_access_token(uid=str(result))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"user_id": result} if result else {"error": "Ошибка регистрации"}

@user_side.post("/login", summary="Вход")
async def login_user(email: str, password: str, response: Response):
    token = login(email, password)
    if token:
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"message": "Вы вошли в аккаунт", "access_token": token } if token else {"error": "Неверные данные"}

@user_side.post("/logout", summary="Выход")
async def logout_user(email: str, response: Response):
    success = logout(email)
    if success:
        response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из аккаунта"} if success else {"error": "Неверные данные"}

@user_side.delete("/delete_account", summary="Удалить аккаунт", dependencies=[Depends(security.access_token_required)])
async def remove_account(password: str, response: Response, request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    success = delete_account(user_id, password)
    if success:
        response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы удалили аккаунт"} if success else {"error": "Неверные данные"}

@user_side.post("/join_course", summary="Присоединиться к курсу", dependencies=[Depends(security.access_token_required)])
async def join_course(course_id: int, request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    success = choose_course(course_id, user_id)
    return {"message": "Вы присоединились к курсу"} if success else {"error": "Неверные данные или вы уже состоите в этом курсе"}

@user_side.post("/quit_course", summary="Покинуть курс", dependencies=[Depends(security.access_token_required)])
async def leave_course(course_id: int, request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    result = quit_course(user_id, course_id)
    return {"message": "Вы вышли из курса"} if result else {"error": "Неверные данные"}

@user_side.post("/submit_hw", summary="Отправить домашнее задание", dependencies=[Depends(security.access_token_required)])
async def submit_homework(hw_id: int, text: str, course_id: int, teacher_id: int, request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    result = add_hw(user_id, hw_id, text, course_id, teacher_id)
    return {"message": "Вы сдали домашнее задание"} if result else {"error": "Неверные данные"}

@user_side.delete("/delete_hw", summary="Удалить домашнее задание", dependencies=[Depends(security.access_token_required)])
async def remove_homework(hw_id: int, request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    success = delete_hw(hw_id, user_id)
    return {"message": "Вы удалили домашнее задание"} if success else {"error": "Неверные данные"}

@user_side.get("/profile", summary="Профиль", dependencies=[Depends(security.access_token_required)])
async def get_profile(request: Request, user_data=Depends(security.access_token_required)):
    user_id = int(user_data.uid)
    profile = profile_user(user_id)
    return {"message": f"Профиль ученика {profile}"} if profile else {"error": "Неверные данные"}
