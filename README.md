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
    - [POST запрос](#post-запрос)
    - [GET запрос](#get-запрос)
    - [PATCH запрос](#patch-запрос)
- [Автор](#автор)


## Описание

Cat Charity Fund - это API для сбора средств, разработанное для поддержки различных целевых проектов, в том числе направленных на помощь популяции кошек. 

Фонд может одновременно вести несколько целевых проектов. У каждого проекта есть название, описание и целевая сумма для сбора. Проекты финансируются по очереди, когда проект набирает необходимую сумму и закрывается, пожертвования начинают поступать в следующий проект.

Пользователи могут делать ненаправленные пожертвования и сопровождать их комментарием. Пожертвования делаются в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который еще не набрал нужную сумму. Если пожертвование больше требуемой суммы или в фонде нет открытых проектов, оставшиеся средства будут ждать открытия следующего проекта.



## Как установить программу

Системные требования:

- Python==3.7.9
- sqlalchemy==1.4.29
- alembic==1.7.7
- fastapi==0.78.0

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
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=<YOUR_SECRET_WORD>
FIRST_SUPERUSER_EMAIL=<SUPERUSER_EMAIL>
FIRST_SUPERUSER_PASSWORD=<SUPERUSER_PASSWORD>
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
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Пример запросов

#### POST запрос
```
http://127.0.0.1:8000/charity_project/
```

Response
```
[
{
"name": "string",
"description": "string",
"full_amount": 100,
"id": 1,
"invested_amount": 10,
"fully_invested": true,
"create_date": "2019-08-24T14:15:22Z",
"close_date": "2019-08-24T14:15:22Z"
}
]
```
#### GET запрос
```
http://127.0.0.1:8000/donation/

```
Request
```
{
"full_amount": 1000,
"comment": "string"
}
```
Response
```
{
"full_amount": 1000,
"comment": "string",
"id": 1,
"create_date": "2019-08-24T14:15:22Z"
}
```
#### PATCH запрос
```
http://127.0.0.1:8000/charity_project/{project_id}

```
Request
```
{
"name": "string",
"description": "string",
"full_amount": 1000
}
```
Response
```
{
"name": "string",
"description": "string",
"full_amount": 1000,
"id": 1,
"invested_amount": 500,
"fully_invested": true,
"create_date": "2019-08-24T14:15:22Z",
"close_date": "2019-08-24T14:15:22Z"
}
```



## Автор 

 * Савельева Анастасия (Visteria09@yandex.ru, https://github.com/Esperansa08) 