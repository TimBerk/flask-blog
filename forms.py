import os

from flask import request, flash
from werkzeug.utils import secure_filename

from wtforms import Form, StringField, BooleanField, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed

from app import app
from models import Tag, Category


def enabled_tags():
    return Tag.query.all()


def enabled_categories():
    return Category.query.all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


class PostForm(Form):
    title = StringField('Название')
    text = CKEditorField('Текст')
    is_published = BooleanField('Опубликовано')
    tags = QuerySelectMultipleField(
        query_factory=enabled_tags,
        get_label=lambda tag: tag.name,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    category = QuerySelectField(
        'Категория',
        query_factory=enabled_categories,
        get_label=lambda category: category.name,
    )
    photo = FileField('Картинка', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Images only!')
    ])

    def valid_photo(self):

        if 'photo' not in request.files:
            flash('Файл не загружен', 'danger')
            return False

        post_file = request.files['photo']
        if post_file.filename == '':
            flash('Файл не выбран', 'danger')
            return False

        if not allowed_file(post_file.filename):
            flash('Неверное расширение ффайла', 'danger')
            return False

        return True

    def upload_photo(self, old_photo=''):
        if not self.valid_photo():
            return False

        post_file = request.files['photo']
        filename = secure_filename(post_file.filename)
        photo = 'photos/' + filename
        post_file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))

        if old_photo:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_photo))

        return photo


class CommentForm(Form):
    text = CKEditorField('Комментарий')
