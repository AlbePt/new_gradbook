# New Gradebook

Это стартовый проект “Отчёты”, включающий **backend** на FastAPI (Python) с использованием SQLAlchemy и Alembic для миграций. Приложение предназначено для ведения электронного журнала: работы со студентами, преподавателями, предметами, оценками, посещаемостью и т. д.

---

## Содержание

1. [Функциональность](#функциональность)  
2. [Технологии](#технологии)  
3. [Требования](#требования)  
4. [Установка и запуск](#установка-и-запуск)  
   - [1. Настройка окружения (Backend)](#1-настройка-окружения-backend)  
   - [2. Выполнение миграций и запуск FastAPI](#2-выполнение-миграций-и-запуск-fastapi)  
5. [Переменные окружения](#переменные-окружения)  
6. [Структура проекта](#структура-проекта)  
7. [Примеры запросов к API](#примеры-запросов-к-api)  
8. [Планы на будущее](#планы-на-будущее)  
9. [Лицензия](#лицензия)

---

## Функциональность

- **CRUD для:**
  - Студентов (`/students`)
  - Преподавателей (`/teachers`)
  - Родителей (`/parents`)
  - Предметов (`/subjects`)
  - Классов (`/classes`)
  - Назначений “преподаватель–предмет” (`/teacher-subjects`)
  - Оценок (`/grades`)
  - Посещаемости (`/attendance`)
  - Расписаний (`/schedules`)
- Роуты FastAPI с Pydantic-схемами (валидация входящих данных, формирование ответов).
- Хранение паролей пользователей через `bcrypt` (Passlib).
- Модели SQLAlchemy с миграциями Alembic (создание/обратное откатывание таблиц).

---

## Технологии

### Backend

- Python 3.10+  
- FastAPI  
- SQLAlchemy ORM  
- Alembic (миграции)  
- Pydantic (валидация и схемы)  
- PostgreSQL (или любая совместимая БД по `DATABASE_URL`)  
- Uvicorn (ASGI-сервер)  
- Passlib (хеширование паролей)


## Требования

1. **Git** (версия ≥ 2.28)  
2. **Python 3.10+**  
3. **PostgreSQL** (или любая другая СУБД, совместимая с SQLAlchemy; строку подключения указывайте в `DATABASE_URL`)  

---

## Установка и запуск

Проект содержит одну директорию:
- `backend/` — код FastAPI  

Ниже описаны шаги для backend.

### 1. Настройка окружения (Backend)

1. Перейдите в папку `backend/`:
   ```bash
   cd backend
````

2. Создайте виртуальное окружение Python и активируйте его:

   * **Windows (PowerShell)**:

     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows (cmd.exe)**:

     ```bat
     python -m venv venv
     venv\Scripts\activate.bat
     ```
   * **macOS / Linux**:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Установите зависимости:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   > **Примечание:** файл `requirements.txt` должен содержать (пример):
   >
   > ```
   > fastapi
   > uvicorn[standard]
   > sqlalchemy
   > alembic
   > psycopg2-binary     # или psycopg2, если предпочитаете
   > pydantic
   > passlib[bcrypt]
   > python-dotenv       # при использовании .env
   > python-multipart    # если понадобятся загрузки файлов
   > ```

4. Создайте файл `.env` (в корне `backend/`) и пропишите в нём переменные окружения (см. раздел [Переменные окружения](#переменные-окружения)).

## Аутентификация

Добавлены эндпоинты `/auth/register` и `/auth/login` для регистрации пользователей и получения JWT токена. В теле запроса при регистрации нужно указать `username`, `password` и `role` (superuser, administrator, teacher, student, parent). Администраторы создаются так же, указывая роль `administrator`, либо через `/users` с этой ролью.

Подробные эскизы интерфейса представлены в [docs/wireframes.md](docs/wireframes.md).

## Импорт отчётов

Формат файлов "Отчёт об успеваемости и посещаемости ученика" описан в
[docs/progress_report_format.md](docs/progress_report_format.md). Чтобы
загрузить такой отчёт в базу, используйте CLI:

```bash
python app/cli.py import progress_report FILE.xlsx
```
