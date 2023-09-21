## Приложение для Благотворительного фонда поддержки котиков

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=for-the-badge&logo=SQLAlchemy&logoColor=ffffff&color=043A6B)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-black?style=for-the-badge)

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Содержание: 
- [Приложение для Благотворительного фонда поддержки котиков](#приложение-для-благотворительного-фонда-поддержки-котиков)
  - [Содержание:](#содержание)
- [Описание](#описание)
- [Как установить программу](#как-установить-программу)
- [Пример запросов](#пример-запросов)
    - [POST запрос - Создание проекта](#post-запрос---создание-проекта)
    - [GET запрос - Получение списка пожертвований](#get-запрос---получение-списка-пожертвований)
    - [PATCH запрос](#patch-запрос)
    - [POST запрос - Создание гугл-таблицы](#post-запрос---создание-гугл-таблицы)
- [Автор](#автор)


## Описание

Cat Charity Fund - это API для сбора средств, разработанное для поддержки различных целевых проектов, в том числе направленных на помощь популяции кошек. 

Фонд может одновременно вести несколько целевых проектов. У каждого проекта есть название, описание и целевая сумма для сбора. Проекты финансируются по очереди, когда проект набирает необходимую сумму и закрывается, пожертвования начинают поступать в следующий проект.

Пользователи могут делать ненаправленные пожертвования и сопровождать их комментарием. Пожертвования делаются в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который еще не набрал нужную сумму. Если пожертвование больше требуемой суммы или в фонде нет открытых проектов, оставшиеся средства будут ждать открытия следующего проекта.

Формирует отчёт в гугл-таблице по закрытым проектам, отсортированным по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Как установить программу

Системные требования:

- Python==3.7.9
- sqlalchemy==1.4.29
- alembic==1.7.7
- fastapi==0.78.0
- aiogoogle==5.5.0

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Esperansa08/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Создать в корневой директории файл .env и заполнить его:

```
APP_TITLE=Сервис для Благотворительного фонда поддержки котиков QRKot
APP_DESCRIPTION=Сервис для поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./catfond.db
SECRET=<YOUR_SECRET_WORD>
FIRST_SUPERUSER_EMAIL=<SUPERUSER_EMAIL>
FIRST_SUPERUSER_PASSWORD=<SUPERUSER_PASSWORD>
TYPE=<TYPE>
PROJECT_ID=<PROJECT_ID>
PRIVATE_KEY_ID=<PRIVATE_KEY_ID>
PRIVATE_KEY=<PRIVATE_KEY>
CLIENT_EMAIL=<CLIENT_EMAIL>
CLIENT_ID=<CLIENT_ID>
AUTH_URI=<AUTH_URI>
TOKEN_URI=<TOKEN_URI>
AUTH_PROVIDER_X509_CERT_URL=<AUTH_PROVIDER_X509_CERT_URL>
CLIENT_X509_CERT_URL=<CLIENT_X509_CERT_URL>
EMAIL=<EMAIL>
```

Выполнить миграции:

```
alembic upgrade head
```

Запустить программу:

```
uvicorn app.main:app --reload

```
После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API досупна по адресам:
- Swagger: [Swagger](http://127.0.0.1:8000/docs)
- Redoc: [Redoc](http://127.0.0.1:8000/redoc)

## Пример запросов

#### POST запрос - Создание проекта
```
http://127.0.0.1:8000/charity_project/

```
Request
```
{
  "name": "Прививки",
  "description": "Сбор на прививки для котят",
  "full_amount": 20000
}
```
Response
```
{
  "name": "Прививки",
  "description": "Сбор на прививки для котят",
  "full_amount": 20000,
  "id": 5,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-09-13T15:25:01.859842"
}
```
#### GET запрос - Получение списка пожертвований
```
http://127.0.0.1:8000/donation/

```
Response
```
[
  {
    "full_amount": 500,
    "comment": "ffds",
    "id": 6,
    "create_date": "2023-09-10T23:17:00.036528",
    "user_id": 1,
    "invested_amount": 500,
    "fully_invested": true,
    "close_date": "2023-09-10T23:17:05"
  },
  {
    "full_amount": 2300,
    "comment": "ex",
    "id": 7,
    "create_date": "2023-09-12T15:14:01.632055",
    "user_id": 1,
    "invested_amount": 2300,
    "fully_invested": true,
    "close_date": "2023-09-12T17:24:01.598221"
  },
  {
    "full_amount": 3000,
    "comment": "ex",
    "id": 8,
    "create_date": "2023-09-12T17:23:58.945923",
    "user_id": 1,
    "invested_amount": 3000,
    "fully_invested": true,
    "close_date": "2023-09-12T23:33:03.477603"
  }
]


```

#### PATCH запрос
```
http://127.0.0.1:8000/charity_project/5

```
Request
```
{
  "name": "Прививки",
  "description": "Сбор на прививки для котят до года",
  "full_amount": 25000
}
```
Response
```
{
  "name": "Прививки",
  "description": "Сбор на прививки для котят до года",
  "full_amount": 25000,
  "id": 5,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-09-13T15:25:01.859842"
}
```
#### POST запрос - Создание гугл-таблицы
```
http://127.0.0.1:8000/google/

```
Response
```
[
  {
    "invested_amount": 10000,
    "fully_invested": true,
    "id": 2,
    "full_amount": 10000,
    "close_date": "2023-09-04T18:05:08",
    "description": "Описание_2",
    "create_date": "2023-09-01T08:05:08",
    "name": "Вакцины"
  },
  {
    "invested_amount": 8000,
    "fully_invested": true,
    "id": 3,
    "full_amount": 8000,
    "close_date": "2023-09-12T13:45:00",
    "description": "Описание_3",
    "create_date": "2023-09-02T22:00:00",
    "name": "Наполнитель"
  },
  {
    "invested_amount": 2000,
    "fully_invested": true,
    "id": 1,
    "full_amount": 2000,
    "close_date": "2023-09-12T10:05:08",
    "description": "Описание_1",
    "create_date": "2023-09-01T10:05:08",
    "name": "На игрушки"
  },
  {
    "invested_amount": 15400,
    "fully_invested": true,
    "id": 4,
    "full_amount": 15400,
    "close_date": "2023-09-18T06:25:08",
    "description": "Описание_4",
    "create_date": "2023-09-05T16:15:08",
    "name": "Еда"
  }
]
```


## Автор 

 * Савельева Анастасия ([Почта](Visteria09@yandex.ru), [Github](https://github.com/Esperansa08)) 