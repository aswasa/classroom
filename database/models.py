from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

tashkent_timezone = pytz.timezone("Asia/Tashkent")


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    password = Column(String)

    courses = relationship("Course", back_populates="teacher", cascade="all, delete", passive_deletes=True, lazy="subquery")
    homeworks = relationship("Homework", back_populates="teacher", cascade="all, delete", passive_deletes=True, lazy="subquery")
    marks = relationship("Mark", back_populates="teacher", cascade="all, delete", passive_deletes=True, lazy="subquery")
    user_homeworks = relationship("UsersHW", back_populates="teacher", cascade="all, delete", passive_deletes=True, lazy="subquery")


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="courses", lazy="subquery")
    homeworks = relationship("Homework", back_populates="course", cascade="all, delete", passive_deletes=True, lazy="subquery")
    user_homeworks = relationship("UsersHW", back_populates="course", cascade="all, delete", passive_deletes=True, lazy="subquery")
    marks = relationship("Mark", back_populates="course", cascade="all, delete", passive_deletes=True, lazy="subquery")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    password = Column(String)
    reg_date = Column(DateTime, default=lambda: datetime.now(tashkent_timezone))
    course_id = Column(Integer, ForeignKey('course.id'))
    course_fk = relationship("Course", lazy="subquery")
    user_homeworks = relationship("UsersHW", back_populates="user", cascade="all, delete", passive_deletes=True, lazy="subquery")
    marks = relationship("Mark", back_populates="user", cascade="all, delete", passive_deletes=True, lazy="subquery")


class Homework(Base):
    __tablename__ = 'hw'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    text = Column(String)
    deadline = Column(String, nullable=True)
    max_mark = Column(Integer)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey('course.id', ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="homeworks", lazy="subquery")
    course = relationship("Course", back_populates="homeworks", lazy="subquery")
    user_homeworks = relationship("UsersHW", back_populates="homework", cascade="all, delete", passive_deletes=True, lazy="subquery")
    marks = relationship("Mark", back_populates="homework", cascade="all, delete", passive_deletes=True, lazy="subquery")


class UsersHW(Base):
    __tablename__ = 'users_hw'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    hw_id = Column(Integer, ForeignKey('hw.id', ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey('course.id', ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    text = Column(String)
    post_time = Column(DateTime, default=lambda: datetime.now(tashkent_timezone))

    user = relationship("User", back_populates="user_homeworks", lazy="subquery")
    homework = relationship("Homework", back_populates="user_homeworks", lazy="subquery")
    course = relationship("Course", back_populates="user_homeworks", lazy="subquery")
    marks = relationship("Mark", back_populates="user_homework", cascade="all, delete", passive_deletes=True, lazy="subquery")
    teacher = relationship("Teacher", back_populates="user_homeworks", lazy="subquery")

class Mark(Base):
    __tablename__ = "mark"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mark = Column(Integer)
    feedback = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    hw_id = Column(Integer, ForeignKey('hw.id', ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey('course.id', ondelete="CASCADE"))
    usershw_id = Column(Integer, ForeignKey('users_hw.id', ondelete="CASCADE"))

    user = relationship("User", back_populates="marks", lazy="subquery")
    teacher = relationship("Teacher", back_populates="marks", lazy="subquery")
    homework = relationship("Homework", back_populates="marks", lazy="subquery")
    course = relationship("Course", back_populates="marks", lazy="subquery")
    user_homework = relationship("UsersHW", back_populates="marks", lazy="subquery")
