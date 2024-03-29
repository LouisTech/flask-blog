from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '080d449909e2aa72ca87a4410ba2d4eadfb475f6c5856c99'

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c2096393:Rooney888!@csmysql.cs.cf.ac.uk:3306/c2096393_blog'
db = SQLAlchemy(app)

from flask_login import LoginManager
login_manager=LoginManager()
login_manager.init_app(app)

#from blog import routes should be at the end
from blog import routes
