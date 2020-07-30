# Простой блог

Простой блог реализован на Flask со связкой MySQL


## Installation

Перед запуском вам необходимо создать базу данных MySQL и записать настройки в config.py

```console
git clone --recursive https://github.com/TimBerk/flask-blog
cd flask-blog/project
pip install -r requirements.txt
python db_init.py
set FLASK_APP=main.py
flask run
```

## Docker

1. Установите docker в вашей ОС
2. Для построения нового образа выполните команду ``docker build . -t blog``
3. Для создания нового контейнера выполните команду ``docker-compose up``

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) -  micro web framework written in Python.
* [Flask-CKEditor](https://flask-ckeditor.readthedocs.io/) - CKEditor integration for Flask.
* [Flask-Login](https://flask-login.readthedocs.io/) - Flask-Login provides user session management for Flask.
* [Flask-Moment](https://github.com/miguelgrinberg/Flask-Moment) - The extension enhances Jinja2 templates with formatting of dates and times using moment.js.
* [Flask-Security](https://pythonhosted.org/Flask-Security/) - The extension adds basic security and authentication features.
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - The extension adds support for SQLAlchemy.
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - The extension integrations WTForms, including CSRF, file upload.
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - The extension integrations WTForms, including CSRF, file upload.


## Features

### Admin backend

* Beautiful and open source dashboard theme for backend SB Admin 2
* Content management components: posts, categories, tags
* Users, Roles

### Users

* Sign in
* Sign up
* Profile editing(personal data)

## Demo User

```
Login: admin@admin.ru
Password: admin
```