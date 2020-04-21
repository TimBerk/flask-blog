# -*- coding: utf8 -*-
from flask_security.utils import encrypt_password

from app import app, user_datastore
from shared import db

from models import User, Role, Post, Tag, Category, Comment


@app.before_first_request
def create_user():
    db.create_all()
    with app.app_context():
        password = encrypt_password('admin')
        user_datastore.create_role(name='admin', description='Administrator')
        user_datastore.create_role(name='user', description='Simple user')
        user_datastore.create_user(email='admin@admin.ru', password=password)

        user = User.query.first()
        role = Role.query.first()
        user_datastore.add_role_to_user(user, role)

        db.session.commit()


if __name__ == "__main__":
    db.drop_all()
    create_user()

    admin = User.query.filter(User.id == 1).first()

    category1 = Category(name='Frontend')
    category2 = Category(name='Backend')
    category3 = Category(name='Live')
    category4 = Category(name='Game')
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)
    db.session.commit()

    tag1 = Tag(name="Css", color=1)
    tag2 = Tag(name="Django", color=2)
    tag3 = Tag(name="Python", color=3)
    tag4 = Tag(name="Google", color=4)
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)
    db.session.commit()

    comment1 = Comment(text='Good post!')
    comment1.author = admin

    p1 = Post(title="Перестаньте использовать !important. Помогаем разобраться с каскадом CSS",
              text="Когда CSS-правило не работает, многие разработчики хотят добавить !important и забыть о проблеме. Рассказываем, почему так делать не стоит и как правильно работать с CSS.")
    p1.author = admin
    p1.is_published = True
    p1.category = category1
    p1.tags.append(tag1)
    p1.comments.append(comment1)

    p2 = Post(title="Facebook выпустит приложение для стриминга игр",
              text="Компания Facebook выпустит приложение для стриминга игр, которое должно стать конкурентом для стриминговых платформ Youtube и Twitch, сообщает NYT, ссылаясь на руководителя приложения Фиджи Симо.")
    p2.author = admin
    p2.is_published = True
    p2.category = category4
    p2.tags.append(tag4)

    p3 = Post(title="Google вводит новые правила в Play Store",
              text="Google Play станет более удобной и &amp;quot;прозрачной&amp;quot; для пользователей. Компания Google планирует обязать разработчиков предоставлять необходимую информацию о бесплатном периоде действия программ, сроках оплаты приложений и дате окончания подписки в простом и понятном для пользователей виде.")
    p3.author = admin
    p3.is_published = True
    p3.category = category3
    p3.tags.append(tag4)

    p4 = Post(title="Uploading Files", text="<p>Ah yes, the good old problem of file uploads. The basic idea of file uploads is actually quite simple. It basically works like this:</p><ol><li><p>A&nbsp;&lt;form&gt;&nbsp;tag is marked with&nbsp;enctype=multipart/form-data&nbsp;and an&nbsp;&lt;input&nbsp;type=file&gt;&nbsp;is placed in that form.</p></li><li><p>The application accesses the file from the&nbsp;files&nbsp;dictionary on the request object.</p></li><li><p>use the&nbsp;<a href=\"https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.FileStorage.save\">save()</a>&nbsp;method of the file to save the file permanently somewhere on the filesystem.</p></li></ol>")
    p4.author = admin
    p4.is_published = True
    p4.category = category2
    p4.tags.append(tag2)
    p4.tags.append(tag3)

    p5 = Post(title="Как живётся студентам на дистанционном обучении: 4 мнения", text="<p><em>С 16 марта вузы начинают переводить своих студентов в режим дистанционного обучения. Для кого-то это временно, но, к примеру, ВШЭ закрыли до лета. Каков первый опыт онлайн-занятий? Мы узнали мнение студентов.</em></p><p><strong>Александр, &laquo;Обществознание и право&raquo;, МПГУ</strong></p><p>Нам сказали, что переведут на дистанционное обучение где-то на месяц, но точных сроков никто не знает. Если честно, я вообще не знаю, как это всё будет происходить. Перевели нас в онлайн-режим уже давно, обещали выслать задания, но так ничего и не прислали, как и всегда у нас в вузе. Я плачу 200 тысяч в год за то, чтобы сидеть на каникулах безо всякой работы. Я волнуюсь за своё образование.</p><p><strong>Карина, &laquo;Государственное управление&raquo;, ВШЭ</strong></p><p>На нашей программе сдача курсовых проходит уже в марте. А библиотеки закрыты, связь с преподавателями нарушена. Я совсем не знаю, как мне завершить свою работу и в каком формате это будет происходить, потому что уехала домой. Ещё переживаю на счёт экономики. Преподаватели этого предмета и так не могут добиться от нас понимания, а теперь, наверное, вообще волосы на себе порвут. Да и мне совсем не хочется отстать.</p>")
    p5.author = admin
    p5.is_published = True
    p5.category = category3

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)

    db.session.commit()
