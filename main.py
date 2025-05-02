from fastapi import FastAPI
from database import engine, Base
from api.teacher import teacher_side
from api.user import user_side

app = FastAPI(docs_url='/')

Base.metadata.create_all(bind=engine)
app.include_router(teacher_side)
app.include_router(user_side)