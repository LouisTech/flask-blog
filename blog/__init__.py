from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '080d449909e2aa72ca87a4410ba2d4eadfb475f6c5856c99'

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2096393:Rooney888!@csmysql.cs.cf.ac.uk:3306/c2096393_blog'
db = SQLAlchemy(app)

from flask_login import LoginManager
login_manager=LoginManager()
login_manager.init_app(app)

from flask_admin import Admin
from blog.models import User, Post, Comment
from blog.views import AdminView
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))

#from blog import routes should be at the end
from blog import routes
