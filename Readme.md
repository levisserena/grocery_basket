
# Grocery_basket

- [О проекте](#about)
- [Стек](#stack)
- [Разворачивание локально](#install)
- [Предварительное наполнение БД](#fill_database)
- [API документация](#API)
- [Информация об авторах](#avtor)

## О проекте <a name="about"></a>

Бэкенд часть интернет магазина. Особенности проекта:
- Продукты в магазине делятся на категории и подкатегории. У каждой категории свой набор подкатегорий. Посмотреть продукты, категории, подкатегории может любой пользователь
- В корзину добавлять, изменять, удалять продукты может только авторизированный пользователь. У каждого пользователя есть доступ только к своей корзины.
- Администратор сервиса может добавлять, изменять или удалять продукты, категории и подкатегории.
- При запросе к корзине выводится поля total_price для каждого продукта в корзине (зависит от количества продуктов) и для корзины в целом.

## При создании проекта использовалось: <a name="stack"></a>
- [Python](https://www.python.org/)
- [Django](https://docs.djangoproject.com/en/5.2/)
- [DRF](https://www.django-rest-framework.org/)
- [Python-Dotenv](https://github.com/theskumar/python-dotenv)
- [pillow](https://pypi.org/project/pillow/)
- [django-imagekit](https://pypi.org/project/django-imagekit/)
- [djangorestframework_simplejwt](https://pypi.org/project/djangorestframework-simplejwt/)
- [drf-spectacular](https://pypi.org/project/drf-spectacular/)

## Разворачивание локально <a name="install"></a>

- Клонировать репозиторий с GitHub:

```
git clone git@github.com:levisserena/grocery_basket.git
```
>[*Активная ссылка на репозиторий*](https://github.com/levisserena/grocery_basket)

- Создать и активировать виртуальное окружение:

Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux
```
python3 -m venv venv
source3 venv/bin/activate
```
- Установить зависимости:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- Настройте файл `.env` согласно `.env.example`
- Установите миграции
```
python grocery_basket/manage.py migrate
```
- Запустите приложение
```
python grocery_basket/manage.py runserver
```

## Предварительное наполнение БД <a name="install"></a>
```
python -Xutf8 grocery_basket/manage.py loaddata grocery_basket/data.json
```

## API документация <a name="API"></a>
В корне проект есть:
- коллекция `GB.postman_collection.json` для [Postman](https://www.postman.com/)
- схема API для [Swagger](https://app.swaggerhub.com)

## Информация об авторах. <a name="avtor"></a>
- Лев Акчурин.<br>
[GitHub](https://github.com/dxndigiden)
