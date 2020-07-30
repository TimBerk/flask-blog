from wtforms import Form, StringField, BooleanField, PasswordField, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from models.role import Role

def enabled_roles():
    return Role.query.all()

class UserForm(Form):
    username = StringField('Логин')
    email = StringField('Email')
    password = PasswordField('Пароль')
    active = BooleanField('Активен')
    roles = QuerySelectMultipleField(
        'Роль',
        query_factory=enabled_roles,
        get_label=lambda role: role.name,
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
