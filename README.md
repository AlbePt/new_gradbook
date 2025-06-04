# New Gradebook

Это стартовый проект “Отчёты”, включающий **backend** на FastAPI (Python) с использованием SQLAlchemy и Alembic для миграций, а также **frontend** на React с Redux для управления состоянием. Приложение предназначено для ведения электронного журнала: работы со студентами, преподавателями, предметами, оценками, посещаемостью и т. д.

---

## Содержание

1. [Функциональность](#функциональность)  
2. [Технологии](#технологии)  
3. [Требования](#требования)  
4. [Установка и запуск](#установка-и-запуск)  
   - [1. Настройка окружения (Backend)](#1-настройка-окружения-backend)  
   - [2. Выполнение миграций и запуск FastAPI](#2-выполнение-миграций-и-запуск-fastapi)  
   - [3. Настройка и запуск React (Frontend)](#3-настройка-и-запуск-react-frontend)  
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
  - Назначений “преподаватель–предмет” (`/teacher-subjects`)
  - Администраторов (`/administrators`)
  - Оценок (`/grades`)
  - Посещаемости (`/attendance`)
  - Расписаний (`/schedules`)
- Роуты FastAPI с Pydantic-схемами (валидация входящих данных, формирование ответов).
- Хранение паролей администраторов через `bcrypt` (Passlib).
- Модели SQLAlchemy с миграциями Alembic (создание/обратное откатывание таблиц).
- CORS Middleware (разрешён доступ с фронтенда, работающего на `http://localhost:3000`).
- Frontend на React:
  - React Router v6 (навигация: список журналов, просмотр, создание, редактирование).
  - Redux Toolkit (хранение списка “журналов” и текущего).
  - Axios для HTTP-запросов к FastAPI.
  - Компоненты: карточки журналов, формы, фильтрация, индикаторы загрузки, уведомления.
  - Стилизация через CSS Modules и глобальные CSS-переменные (variables.css, globals.css).

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

### Frontend

- Node.js 16+ (рекомендуется LTS)  
- React 18+  
- React Router v6  
- Redux Toolkit (RTK)  
- Axios  
- CSS Modules (локальные стили)  
- Tailwind (опционально, если захотите)  
- Библиотека иконок `react-icons` для иконки поиска

---

## Требования

1. **Git** (версия ≥ 2.28)  
2. **Python 3.10+**  
3. **Node.js** (версия ≥ 16 LTS) и npm/yarn  
4. **PostgreSQL** (или любая другая СУБД, совместимая с SQLAlchemy; строку подключения указывайте в `DATABASE_URL`)  

---

## Установка и запуск

Проект разделён на две директории:  
- `backend/` — код FastAPI  
- `frontend/` — код React 

Ниже описаны шаги для оба́х частей.

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

Добавлены эндпоинты `/auth/register` и `/auth/login` для регистрации пользователей и получения JWT токена. В теле запроса при регистрации нужно указать `username`, `password` и `role` (superuser, administrator, teacher, student, parent).




## Настройка и запуск React (Frontend)

1. Перейдите в папку `frontend/` и установите зависимости (требуется Node.js 16+):

```bash
cd frontend
npm install
```

2. Запустите дев‑сервер:

```bash
npm run start
```

Приложение будет доступно на `http://localhost:3000`.

Проект использует Redux Toolkit и разделён по сущностям в папке `src/components`. Общая маршрутизация админки находится в `src/routes/AdminRoutes.jsx`.

Подробные эскизы интерфейса представлены в [docs/wireframes.md](docs/wireframes.md).
