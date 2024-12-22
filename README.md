# PythonSalonDjango

**PythonSalonDjango** — это веб-приложение на основе Django, предназначенное для управления салоном красоты. Имеет функциональность для управления услугами, сотрудниками, клиентами и записями на прием.

## Особенности

- **Управление услугами**: создание, редактирование и удаление услуг, предоставляемых салоном.
- **Управление сотрудниками**: добавление, редактирование и удаление информации о сотрудниках.
- **Управление клиентами**: хранение информации о клиентах и их предпочтениях.
- **Запись на прием**: планирование и управление записями клиентов на услуги.

## Требования

- Python 3.8+
- Django 4.2+
- Django REST Framework

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/GoNt1eRRR/PythonSalonDjango
cd PythonSalonDjango
```
2. Создайте виртуальное окружение:

```bash
python3 -m venv env
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

Установите зависимости:

```
pip install -r requirements.txt
```
Примените миграции базы данных:
```
python manage.py migrate
```

Создайте суперпользователя для доступа к административной панели:
```
python manage.py createsuperuser
```
Запустите сервер разработки:
```
python manage.py runserver
```

## Структура проекта:

* beauty_salon/ — основной модуль проекта.
* api/ — модуль, содержащий реализацию API.
* django_bot/ — модуль, отвечающий за интеграцию с Telegram-ботом для уведомлений и взаимодействия с клиентами.
* manage.py — скрипт для управления проектом.
* requirements.txt — файл с перечнем зависимостей проекта.

## API
### Users
- `GET /api/users/`: Получить список всех пользователей
- `POST /api/users/`: Создать нового пользователя
- `GET /api/users/{id}/`: Получить данные пользователя по ID
- `PATCH /api/users/{id}/`: Обновить данные пользователя
- `DELETE /api/users/{id}/`: Удалить пользователя

### Salons
- `GET /api/salons/`: Получить список всех салонов
- `POST /api/salons/`: Создать новый салон
- `GET /api/salons/{id}/`: Получить информацию о салоне по ID
- `PATCH /api/salons/{id}/`: Обновить данные салона
- `DELETE /api/salons/{id}/`: Удалить салон

### Procedures
- `GET /api/procedures/`: Получить список всех процедур
- `POST /api/procedures/`: Добавить новую процедуру
- `GET /api/procedures/{id}/`: Получить информацию о процедуре по ID
- `PATCH /api/procedures/{id}/`: Обновить данные процедуры
- `DELETE /api/procedures/{id}/`: Удалить процедуру

### Specialists
- `GET /api/specialists/`: Получить список всех специалистов
- `POST /api/specialists/`: Добавить нового специалиста
- `GET /api/specialists/{id}/`: Получить информацию о специалисте по ID
- `PATCH /api/specialists/{id}/`: Обновить данные специалиста
- `DELETE /api/specialists/{id}/`: Удалить специалиста

### Availabilities
- `GET /api/availabilities/`: Получить список всех доступных временных слотов
- `POST /api/availabilities/`: Добавить новый временной слот
- `GET /api/availabilities/{id}/`: Получить информацию о временном слоте по ID
- `PATCH /api/availabilities/{id}/`: Обновить данные временного слота
- `DELETE /api/availabilities/{id}/`: Удалить временной слот

### Bookings
- `GET /api/bookings/`: Получить список всех записей
- `POST /api/bookings/`: Создать новую запись
- `GET /api/bookings/{id}/`: Получить информацию о записи по ID
- `PATCH /api/bookings/{id}/`: Обновить данные записи
- `DELETE /api/bookings/{id}/`: Удалить запись

## Модели

### CustomUser
Расширенная версия `AbstractUser` с дополнительными полями:
- **Поля**: `telegram_id`, `phone_number`, `role`, `groups`, `user_permissions`.

---

### Salon
Представляет салон.
- **Поля**: `name`, `address`.

---

### Procedure
Представляет процедуру, предлагаемую салоном.
- **Поля**: `name`, `description`, `price`.

---

### Specialist
Представляет специалиста, предоставляющего процедуры.
- **Связь**: Один-к-одному с `CustomUser`, многие-ко-многим с `Salon`, многие-ко-многим с `Procedure`.
- **Поля**: `user`, `salons`, `procedures`.

---

### Availability
Представляет доступность специалиста в салоне.
- **Связь**: Внешний ключ на `Specialist`, внешний ключ на `Salon`.
- **Поля**: `specialist`, `salon`, `start_time`, `end_time`, `is_booked`.

---

### Booking
Представляет бронь, сделанную клиентом.
- **Связь**: Внешний ключ на `CustomUser`, `Salon`, `Procedure`, `Availability`.
- **Поля**: `client`, `salon`, `procedure`, `availability`, `price`, `phone_number`, `created_at`, `confirmed`.

---
## Админ-панель
Панель администратора доступна по адресу /admin/ для управления всеми моделями

