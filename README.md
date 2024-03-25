# QRkot_spreadseets

<h4>QRKot - это приложение для благотворительного фонда поддержки котиков. С его помощью вы можете сделать онлайн-пожертвование, которое пойдет на обеспечение нужд всех видов кошек и котят!</h4>

Доступны следующие функции: создание, редактирование, удаление и получение проектов, отправка пожертвований и получение информации о них, регистрация и авторизация пользователей. Также есть возможность вывести информацию о закрытых проектах в google таблицу.

---

## Как скачать и запустить проект:
1. **Клонировать репозиторий и перейти в папку с ним:**

```bash
git clone git@github.com:dasha2000vas/cat_charity_fund.git
cd cat_charity_fund
```

2. **Создать и заполнить файл .env:**

```python
EMAIL=почта_которой_будет_предоставлен_доступ_к_таблице
```

Получить JSON-файл с ключом доступа к сервисному аккаунту на Google Cloud Platform. Перенести информацию из этого файла в .env:

```python
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```


3. **Создать и активировать виртуальное окружение:**

```bash
python -m venv venv
source venv/Scripts/activate
```

4. **Установить зависимости из файла requirements.txt:**

```bash
pip install -r requirements.txt
```

5. **Применить миграции для таблиц:**
```bash
alembic upgrade head
```

6. **Запустить сервер Uvicorn:**
```bash
uvicorn app.main:app
```

---

## Примеры запросов:
1. **Эндпоинт: http://127.0.0.1:8000/auth/register. Метод запроса: POST<br>Права доступа: доступно без токена**

    При передаче следующих данных:

    * "email": "user@example.com" (required),
    * "password": "string" (required)
   
    Вы получите ответ о создании нового пользователя:
  
    * "id": 1,
    * "email": "user@example.com" (required),
    * "is_active": true,
    * "is_superuser": false,
    * "is_verified": false

<br>

2. **Эндпоинт: http://127.0.0.1:8000/users/me. Метод запроса: GET<br>Права доступа: авторизованный пользователь** 

    В ответ вы получите информацию о текущем пользователе:

    * "id": 1,
    * "email": "user@example.com" (required),
    * "is_active": true,
    * "is_superuser": false,
    * "is_verified": false

<br>

3. **Эндпоинт: http://127.0.0.1:8000/charity_project. Метод запроса: GET<br>Права доступа: доступно без токена**

    В ответ вы получите список всех благотворительных проектов.

<br>

4. **Эндпоинт: http://127.0.0.1:8000/charity_project. Метод запроса: POST<br>Права доступа: администратор**

    При передаче следующих данных:

    * "name": "string" (required),
    * "description": "string" (required),
    * "full_amount": 100 (required)

    Вы получите ответ о создании нового благотворительного проекта:

    * "name": "string" (required),
    * "description": "string" (required),
    * "full_amount": 100 (required),
    * "id": 1 (required),
    * "invested_amount": 0 (required),
    * "fully_invested": false (required),
    * "create_date": "2024-03-16T14:15:22Z" (required),
    * "close_date": null

На счет проекта тут же поступят все свободные пожертвования(при их наличии).

<br>

5. **Эндпоинт: http://127.0.0.1:8000/donation. Метод запроса: POST<br>Права доступа: авторизованный пользователь**

    При передаче следующих данных:
    * "full_amount": 100 (required),
    * "comment": "string"

    Вы получите ответ о сделанном пожертвовании:

    * "full_amount": 100 (required),
    * "comment": "string",
    * "id": 1 (required),
    * "create_date": "2024-03-16T14:15:22Z" (required)

Сумма тут же запишется на счёт первого открытого проекта(при его наличии).

<br>

6. **Эндпоинт: http://127.0.0.1:8000/donation. Метод запроса: GET<br>Права доступа: авторизованный пользователь**

  В ответ вы получите список всех пожертвований текущего пользователя.

7. **Эндпоинт:http://127.0.0.1:8000/google. Метод запроса: POST<br>Права доступа: администратор**

  В ответ вы получите список закрытых проектов, отсортированных по возрастанию времени сбора средств. О каждом будет представлена следующая информация:

   * "name": "string" (required),
   * "collection_time": "10 days, 10:10:10.10" (required),
   * "description": "string" (required)

  Также будет создана google таблица, в которую запишутся все полученные данные. Доступ к файлу будет аккаунта почты, указанного в .env.



---

## Технический стек:
* aiosqlite0.17.0
* aiogoogle4.2.0
* alembic1.7.7
* fastapi0.78.0
* fastapi-users[sqlalchemy]10.0.4
* sqlalchemy1.4.36
* uvicorn[standard]0.17.6

---

## Автор:
Василевская Дарья

---

## Примечание:

>**Ознакомиться с документацией API ближе можно по ссылке http://127.0.0.1:8000/docs**
