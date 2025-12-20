# FastAPI Microservices

Этот репозиторий содержит два микросервиса на FastAPI с использованием SQLite:

1. **TODO Service** – управление списком задач (CRUD)
2. **Short URL Service** – генерация и управление короткими ссылками

---

## Технологический стек

- Python 3.11
- FastAPI — веб-фреймворк для создания API
- Uvicorn — ASGI-сервер
- SQLite — легковестная база данных
- Pydantic — схемы и валидация
- Docker — контейнеризация
- Swagger — тестирование API

---

## Диаграмма

![alt text](images/image.png)

---

## Структура проекта

```
.
├── todo/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
├── shorturl/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

---

## Установка и запуск

### Через Docker

1. Постройте образ:

```bash
docker build -t todo ./todo
docker build -t shorturl ./shorturl
```

2. Запустите контейнер с volume для данных:

```bash
docker run -d -p 8000:80 -v todo_data:/app/data todo_service
docker run -d -p 8001:80 -v shorturl_data:/app/data shorturl_service
```

- TODO сервис → `http://localhost:8000`
- Short URL сервис → `http://localhost:8001`

---

## Документация

- TODO сервис → `http://localhost:8000/docs`
- Short URL сервис → `http://localhost:8001/docs`

---

## TODO Service

### Методы API

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/items` | Создать задачу |
| `GET` | `/items` | Получить все задачи |
| `GET` | `/items/{item_id}` | Получить задачу по ID |
| `GET` | `/items/status?completed=true` | Фильтрация по статусу |
| `PUT` | `/items/{item_id}` | Обновить задачу |
| `DELETE` | `/items/{item_id}` | Удалить задачу |
| `GET` | `/items/search?q=<text>` | Поиск по заголовку и описанию |
| `GET` | `/items/stats` | Статистика задач (total, completed, pending) |

---

### Демонстрация работы

1. Создание записи
![alt text](images/image-1.png)

2. Получение всех записей
![alt text](images/image-2.png)

3. Поиск записи по названию
![alt text](images/image-3.png)

4. Поиск по полю completed
![alt text](images/image-4.png)

5. Получение записи по id
![alt text](images/image-5.png)

6. Удаления записи по id
![alt text](images/image-6.png)

7. Обновления записи по id
![alt text](images/image-7.png)

---

## Short URL Service

### Методы API

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/shorten` | Создать короткую ссылку |
| `GET` | `/{short_id}` | Перейти по короткой ссылке (редирект) |
| `GET` | `/stats/{short_id}` | Получить статистику ссылки |
| `PUT` | `/urls/{short_id}` | Обновить полную ссылку |
| `GET` | `/urls/popular` | Получить самые популярные ссылки |

---

### Демонстрация работы

1. Создания короткой ссылки
![alt text](images/image-8.png)

2. Редирект 
![alt text](images/image-9.png)
![alt text](images/image-10.png)

3. Статистика по ссылки
![alt text](images/image-11.png)

4. Получаем популярные ссылки
![alt text](images/image-12.png)