from app import app
import view

from admin.blueprint import admin
from admin.posts.blueprint import posts
from posts.blueprint import user_posts
from admin.users.blueprint import users
from admin.tags.blueprint import tags
from admin.categories.blueprint import categories

if __name__ == "__main__":

    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user_posts, url_prefix='/posts')
    app.register_blueprint(posts, url_prefix='/admin/posts')
    app.register_blueprint(users, url_prefix='/admin/users')
    app.register_blueprint(tags, url_prefix='/admin/tags')
    app.register_blueprint(categories, url_prefix='/admin/categories')

    app.run(debug=True)
