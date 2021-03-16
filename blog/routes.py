import re
from flask import render_template, url_for, request, redirect, flash
from flask_login.utils import login_required, logout_user
from blog.models import User, Post, Comment, Rating
from blog import app, db
from blog.forms import LoginForm, RegistrationForm, CommentForm, SearchForm, RatingForm
from flask_login import current_user, login_user, logout_user


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm(request.form)
    if request.method == 'POST':
        searched = form.search.data
        posts = Post.query.filter(Post.title.contains(searched) | Post.content.contains(searched))
    else:
        posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts, search_form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    return render_template('post.html', title=post.title, post=post, comments=comments, comment_form=comment_form, rating_form=rating_form)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    if comment_form.validate_on_submit():
        db.session.add(Comment(content=comment_form.comment.data, post_id = post.id, author_id=current_user.id))
        db.session.commit()
        flash('Your comment has been added to the post', 'success')
        return redirect(f'/post/{post.id}')
    
    comments = Comment.query.filter(Comment.post_id == post.id)
    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, rating_form=rating_form)

@app.route('/post/<int:post_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_post(post_id):
    print("worked1", flush=True)
    post = Post.query.get_or_404(post_id)
    rating_form = RatingForm()
    comment_form = CommentForm()
    comments = Comment.query.filter(Comment.post_id == post.id)
    if rating_form.validate_on_submit():
        print("worked", flush=True)
        db.session.add(Rating(rating=rating_form.rating.data, rater_id=current_user.id, post_id = post.id))
        db.session.commit()
        flash('Your rating has been added to the post', 'success')
        return redirect(f'/post/{post.id}')
    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, rating_form=rating_form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    flash('Invalid email address or password.')
    return render_template('login.html', title='Login', form=form)

#This page needs testing!
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))