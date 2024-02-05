Описание: 
API для социальной сети, который позволяет пользователям, создавать записи о произведениях, писать отзывы на записи,  комментировать отзывы.

Стек:
Python
Django REST Framework
JWT-tokens

Как запустить проект:
Клонировать репозиторий:

git clone https://github.com/kise2k/api_yambd.git

перейти в него в командной строке:

cd api_yambd/

Создавть и активировать виртуальное окружение:

python -m venv venv
source venv/scripts/activate

Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции:

cd api_yambd
python manage.py migrate

Запустить проект:

python manage.py runserver

Алгоритм регистрации пользователя:
1) Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2) YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3) Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4) При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле.

Примеры ответа:

GET-запрос
api/v1/categories/

{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}

POST-запрос
api/v1/titles/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}

После запуска проекта, документация будет доступна по адресу:
http://localhost:port/redoc/

Авторы: Седякин Кирилл Игоревич, Хоменко Анна Олеговна, Ким Данил Андреевич
Ссылка на github: https://github.com/kise2k
