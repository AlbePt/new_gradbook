# backend/main.py
from fastapi import FastAPI
from core.db import engine, Base

# Импорт моделей для регистрации в metadata
from models import student, teacher, subject, teacher_subject, parent, grade, schedule, attendance, administrator, user  # noqa

# Импорт роутеров
from routers.student_router import router as student_router
from routers.teacher_router import router as teacher_router
from routers.subject_router import router as subject_router
from routers.teacher_subject_router import router as teacher_subject_router
from routers.parent_router import router as parent_router
from routers.grade_router import router as grade_router
from routers.schedule_router import router as schedule_router
from routers.class_router import router as class_router
from routers.attendance_router import router as attendance_router
from routers.administrator_router import router as administrator_router
from routers.region_router import router as region_router
from routers.city_router import router as city_router
from routers.school_router import router as school_router
from routers.academic_year_router import router as academic_year_router
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router


from fastapi.middleware.cors import CORSMiddleware 


app = FastAPI(title="Gradebook API")

# Добавить CORS middleware перед регистрацией роутеров
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешить фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрация роутеров
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(teacher_subject_router)
app.include_router(parent_router)
app.include_router(grade_router)
app.include_router(schedule_router)
app.include_router(class_router)
app.include_router(attendance_router)
app.include_router(administrator_router)
app.include_router(region_router)
app.include_router(city_router)
app.include_router(school_router)
app.include_router(academic_year_router)
app.include_router(user_router)
app.include_router(auth_router)

# При необходимости создания таблиц без миграций
# Base.metadata.create_all(bind=engine)


# backend/alembic.ini
# ------
# [alembic]
# script_location = backend/alembic
# sqlalchemy.url = %(DATABASE_URL)s
#
# [loggers]
# keys = root,sqlalchemy,alembic
#
# [handlers]
# keys = console
#
# [formatters]
# keys = generic
#
# [logger_root]
# level = WARN
# handlers = console
#
# [logger_sqlalchemy]
# level = INFO
# handlers = console
# qualname = sqlalchemy.engine
#
# [logger_alembic]
# level = INFO
# handlers = console
# qualname = alembic
#
# [handler_console]
# class = StreamHandler
# args = (sys.stderr,)
# level = NOTSET
# formatter = generic
#
# [formatter_generic]
# format = %(levelname)-5.5s [%(name)s] %(message)s
