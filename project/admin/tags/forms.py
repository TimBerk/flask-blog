from wtforms import Form, StringField, RadioField
from models.tag import COLORS


class TagForm(Form):
    name = StringField('Название')
    color = RadioField('Цвет', choices=COLORS)
