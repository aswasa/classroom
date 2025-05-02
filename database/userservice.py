from database import get_db
from database.models import Teacher, User, Course, Homework, UsersHW

def register(username, phone_number, email, password):
    with next(get_db()) as db:
        try:
            new_user = Teacher(username=username, phone_number=phone_number,
                            email=email, password=password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user.id
        except Exception as e:
            db.rollback()
            return {"error": f"Ошибка при добавлении: {str(e)}"}

def login(email, password):
    with next(get_db()) as db:
        user = db.query(Teacher).filter_by(email=email).first()
        if user and user.password==password:
            return True
        else:
            return False

def logout(email):
    with next(get_db()) as db:
        action = db.query(User).filter_by(email=email).first()
        if action:
            return True
        else:
            return False

def delete_account(email, password):
    with next(get_db()) as db:
        user = db.query(Teacher).filter_by(email=email).first()
        if user and user.password==password:
            db.delete(user)
            db.commit()
            return True
        return False

# def choose_course(course_id, user_id):
#     with next(get_db()) as db:
#         user = db.query(User).filter_by(id=user_id).first()
#         course = db.query(Course).filter_by(id=course_id).first()
#         if not user:
#             return False
#         if not course:
#             return False
#         if user.course_id == course_id:
#             return False #уже состоит в этом курсе
#         user.course_id = course_id
#         db.commit()
#         return True
#
# def quit_course(user_id, course_id):
#     with next(get_db()) as db:
#         user = db.query(User).filter_by(id=user_id).first()
#         if user and user.course_id==course_id:
#             user.course_id = None
#             db.commit()
#             return True
#         return False # пользователь не был на курсе
#
# def add_hw(user_id, hw_id, text, course_id, teacher_id):
#     with next(get_db()) as db:
#         user = db.query(User).filter_by(id=user_id).first()
#         hw = db.query(Homework).filter_by(id=hw_id).first()
#         course = db.query(Course).filter_by(id=course_id).first()
#         teacher = db.query(Teacher).filter_by(id=teacher_id).first()
#         if not all([user, hw, course, teacher]):
#             return False
#
#         try:
#             submission = UsersHW(
#                 user_id=user_id,
#                 hw_id=hw_id,
#                 text=text,
#                 course_id=course_id,
#                 teacher_id=teacher_id
#             )
#             db.add(submission)
#             db.commit()
#             db.refresh(submission)
#             return True
#         except Exception as e:
#             db.rollback()
#             return False
#
#
# def delete_hw(hw_id, user_id):
#     with next(get_db()) as db:
#         submission = db.query(UsersHW).filter_by(hw_id=hw_id, user_id=user_id).first()
#         if submission:
#             db.delete(submission)
#             db.commit()
#             return True
#         return False

def choose_course(course_id, user_id):
    with next(get_db()) as db:
        user = db.query(User).filter_by(id=user_id).first()
        course = db.query(Course).filter_by(id=course_id).first()

        if not user or not course:
            return False

        if user.course_id == course_id:
            return False

        user.course_id = course_id
        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Ошибка при добавлении в курс: {e}")
            return False


def quit_course(user_id, course_id):
    with next(get_db()) as db:
        user = db.query(User).filter_by(id=user_id).first()
        if user and user.course_id == course_id:
            user.course_id = None
            try:
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                return False
        return False


def add_hw(user_id, hw_id, text, course_id, teacher_id):
    with next(get_db()) as db:
        user = db.query(User).filter_by(id=user_id).first()
        hw = db.query(Homework).filter_by(id=hw_id).first()
        course = db.query(Course).filter_by(id=course_id).first()
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()

        if not all([user, hw, course, teacher]):
            return False

        try:
            submission = UsersHW(
                user_id=user_id,
                hw_id=hw_id,
                text=text,
                course_id=course_id,
                teacher_id=teacher_id
            )
            db.add(submission)
            db.commit()
            db.refresh(submission)
            return True
        except Exception as e:
            db.rollback()
            print(f"Ошибка при добавлении домашнего задания: {e}")
            return False


def delete_hw(hw_id, user_id):
    with next(get_db()) as db:
        submission = db.query(UsersHW).filter_by(hw_id=hw_id, user_id=user_id).first()
        if submission:
            try:
                db.delete(submission)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                return False
        return False


def profile_user(user_id):
    with next(get_db()) as db:
        profile = db.query(User).filter_by(id=user_id).first()
        if profile:
            return True
        else:
            return False
