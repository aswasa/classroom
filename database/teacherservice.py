from database import get_db
from database.models import Teacher, User, Course, Homework, Mark
from typing import Optional
from auth_config import security


def register(username, phone_number, email, password):
    with next(get_db()) as db:
        try:
            new_teacher = Teacher(username=username, phone_number=phone_number,
                            email=email, password=password)
            db.add(new_teacher)
            db.commit()
            return new_teacher.id
        except Exception as e:
            db.rollback()
            return {"error": f"Ошибка при добавлении: {str(e)}"}


def login(email, password):
    with next(get_db()) as db:
        user = db.query(Teacher).filter_by(email=email).first()
        if user and user.password==password:
            token = security.create_access_token(uid=str(user.id))
            return token
        else:
            return False

def delete_account(teacher_id, password):
    with next(get_db()) as db:
        user = db.query(Teacher).filter_by(id=teacher_id).first()
        if user and user.password==password:
            db.delete(user)
            db.commit()
            return True
        return False

def logout(email):
    with next(get_db()) as db:
        action = db.query(Teacher).filter_by(email=email).first()
        if action:
            return True
        else:
            return False

def create_course(name, description, teacher_id):
    with next(get_db()) as db:
        course = db.query(Course).filter_by(name=name).first()
        if course:
            return False  # уже есть такой курс
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()
        if not teacher:
            return False

        new_course = Course(name=name, description=description, teacher_id=teacher_id)
        db.add(new_course)
        db.commit()
        return new_course.id


def delete_course(name, teacher_id):
    with next(get_db()) as db:
        course = db.query(Course).filter_by(name=name).first()
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()
        if course and teacher:
            db.delete(course)
            db.commit()
            return True
        return False

def add_hw(teacher_id, title, text, deadline, max_mark):
    with next(get_db()) as db:
        hw = db.query(Homework).filter_by(title=title).first()
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()
        if hw and teacher:
            return False
        new_hw = Homework(teacher_id=teacher_id, title=title, text=text, deadline=deadline, max_mark=max_mark)
        db.add(new_hw)
        db.commit()
        return new_hw.id

def delete_hw(title, teacher_id):
    with next(get_db()) as db:
        hw = db.query(Homework).filter_by(title=title).first()
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()
        if hw and teacher:
            db.delete(hw)
            db.commit()
            return True
        return False

def redact_hw(title, new_text, new_deadline, teacher_id):
    with next(get_db()) as db:
        hw = db.query(Homework).filter_by(title=title, teacher_id=teacher_id).first()
        if not hw:
            return False
        hw.text = new_text
        hw.deadline = new_deadline
        db.commit()
        return True

def check_hw(hw_id, mark, user_id, teacher_id, feedback: Optional[str] = None):
    with next(get_db()) as db:
        mark = db.query(Mark).filter_by(hw_id=hw_id)
        if mark:
            return False
        teacher = db.query(Teacher).filter_by(id=teacher_id).first()
        user = db.query(User).filter_by(id=user_id).first()
        hw = db.query(Homework).filter_by(id=hw_id).first()
        if all([teacher, user, hw]):
            new_mark = Mark(mark=mark, feedback=feedback,
                            user_id=user_id, hw_id=hw_id, teacher_id=teacher_id)
            db.add(new_mark)
            db.commit()
            return new_mark.id

def profile_teacher(teacher_id):
    with next(get_db()) as db:
        profile = db.query(Teacher).filter_by(id=teacher_id).first()
        if profile:
            return True
        else:
            return False