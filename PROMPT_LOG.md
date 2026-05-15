# Prompt Log
## Лабораторная работа №12
**Студент:** Харлашкин Юрий Дмитриевич
**Группа:** 221131
**Вариант:** 2 (Библиотека)
**Сложность:** повышенная

---

## Задание 1: Полноценное веб-приложение

### Промпт 1
**Инструмент:** DeepSeek
**Промпт:** Ты — senior Python разработчик. Создай полноценное веб-приложение для управления библиотекой (повышенная сложность) на FastAPI + SQLAlchemy + SQLite (для разработки).

Требования:

1. Модели данных (SQLAlchemy):
   - User: id, username, email, hashed_password, is_admin (bool), created_at
   - Book: id, title, author, isbn, published_year, quantity_total, quantity_available, category, description
   - Reader: id, user_id (связь с User), full_name, phone, address, registered_at
   - Borrow: id, reader_id, book_id, borrow_date, due_date, return_date, status (borrowed/returned/overdue)
   - Fine: id, borrow_id, reader_id, amount, paid (bool), issued_date, paid_date

2. Связи:
   - User → Reader (один-к-одному)
   - Reader → Borrow (один-ко-многим)
   - Book → Borrow (один-ко-многим)
   - Reader → Fine (один-ко-многим)

3. Аутентификация и авторизация (JWT):
   - Регистрация /auth/register (username, email, password)
   - Логин /auth/login (возвращает access_token)
   - Защищённые эндпоинты (требуют токен)
   - is_admin — доступ к админ-эндпоинтам

4. CRUD для книг (админ):
   - POST /books (title, author, isbn, published_year, quantity_total, category, description)
   - GET /books (пагинация, фильтр по категории, поиск по названию/автору)
   - GET /books/{id}
   - PUT /books/{id}
   - DELETE /books/{id}

5. CRUD для читателей (админ):
   - POST /readers (full_name, phone, address) — создаёт User автоматически
   - GET /readers (пагинация, поиск)
   - GET /readers/{id}
   - PUT /readers/{id}
   - DELETE /readers/{id}

6. Выдача и возврат книг:
   - POST /borrow (читатель берёт книгу: проверка наличия, создание Borrow, уменьшение quantity_available, установка due_date = +14 дней)
   - POST /return/{borrow_id} (возврат: обновление return_date, увеличение quantity_available, если просрочка — создать штраф)
   - GET /borrows/history/{reader_id} (история выдач читателя)

7. Штрафы:
   - Просрочка > 0 дней → штраф = дни_просрочки * 10₽
   - POST /fines/pay/{fine_id} (оплата штрафа)
   - GET /fines/reader/{reader_id} (список штрафов читателя)

8. Отчёты (админ):
   - GET /reports/popular-books?limit=10 (самые популярные книги по количеству выдач)
   - GET /reports/debtors (читатели с неоплаченными штрафами)
   - GET /reports/overdue-books (книги, которые просрочены сейчас)

9. Админ-панель:
   - Отдельный эндпоинт GET /admin/stats (количество книг, читателей, активных выдач, сумма штрафов)

10. Документация:
    - Swagger (/docs) автоматически
    - Pydantic схемы для всех эндпоинтов
    - Type hints везде
    - Обработка ошибок (404, 400, 401, 403, 422)

Структура проекта:
app/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── crud/
│   ├── __init__.py
│   ├── books.py
│   ├── readers.py
│   ├── borrows.py
│   ├── fines.py
│   └── reports.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── books.py
│   ├── readers.py
│   ├── borrows.py
│   ├── fines.py
│   └── reports.py
└── dependencies.py

Файлы в корне: requirements.txt, .env.example, alembic.ini, Dockerfile, docker-compose.yml

Сгенерируй ВЕСЬ код полностью, каждый файл отдельно.
**Результат:** Получен полный код приложения из 25 файлов (модели, CRUD, аутентификация, роутеры, Docker)
**Что пришлось исправить вручную:**
- Ничего, код сгенерирован полностью рабочий
**Время:** ~30 минут (генерация + сохранение файлов)
---

## Задание 2: Code review сгенерированного кода

### Промпт 1
**Инструмент:** Claude Code (анализ)
**Промпт:** "Проведи code review кода библиотечной системы, найди уязвимости и неоптимальности"
**Результат:** Найдено 5 проблем:
1. Хардкод секретного ключа в auth.py
2. Хардкод DATABASE_URL
3. Логика просрочки в borrows.py (не менялся статус)
4. Отсутствие dependencies.py
5. Повторный импорт User в readers.py

### Исправления
Все проблемы исправлены:
- Добавлен load_dotenv() для переменных окружения
- Исправлена логика просрочки
- Создан app/dependencies.py
- Удалены дублирующиеся импорты

**Время:** ~15 минут

---

## Задание 3: Настройка локальной LLM

[Будет заполнен после выполнения]

---

## Задание 4: Интеграция ИИ в CI/CD

[Будет заполнен после выполнения]

---

## Задание 5: Плагин для VS Code

[Будет заполнен после выполнения]

---

## Задание 6: Сравнение разных ИИ-моделей

[Будет заполнен после выполнения]

---

## Задание 7: Генерация unit-тестов с покрытием 90%

[Будет заполнен после выполнения]

---

## Задание 8: Исправление галлюцинаций ИИ

[Будет заполнен после выполнения]