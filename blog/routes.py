from flask import render_template, url_for
from blog.models import User, Post
from blog import app


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')
