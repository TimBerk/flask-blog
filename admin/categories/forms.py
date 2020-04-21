from wtforms import Form, StringField


class CategoryForm(Form):
    name = StringField('Название')
    slug = StringField('Slug')
