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
    # Get first four posts latest first
    posts = Post.query.all()
    four_posts = []
    for i in range(len(posts)-1,len(posts)-5,-1):
        four_posts.append(posts[i])
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        return redirect(url_for('posts', search_form = searched))
    return render_template('home.html', title='LT | Home', posts=four_posts, search_form=search_form)

@app.route("/posts", methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        posts = Post.query.filter(Post.title.contains(searched) | Post.content.contains(searched))
    else:
        posts = Post.query.all()
    #format post dates
    return render_template('posts.html', title='LT | Posts', posts=posts, search_form=search_form)


@app.route("/about", methods=['GET', 'POST'])
def about():
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        return redirect(url_for('posts', search_form=searched))
    return render_template('about.html', title='LT | About', search_form=search_form)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        return redirect(url_for('posts', search_form=searched))

    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id == post.id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    #Calculate average rating
    avg_rating = 0.0
    user_rating=None
    if current_user.is_authenticated:
        user_rating = Rating.query.filter_by(rater_id=current_user.id, post_id=post.id).first()
        if not user_rating:
            user_rating = "Not Rated"
        else:
            user_rating = str(user_rating.rating)

    all_ratings = Rating.query.filter_by(post_id=post.id).all()
    if all_ratings:
        for i in range(len(all_ratings)):
            avg_rating += all_ratings[i].rating
        avg_rating /= len(all_ratings)
    return render_template('post.html', title=post.title, search_form=search_form, post=post, comments=comments, comment_form=comment_form, rating_form=rating_form, avg_rating=avg_rating, user_rating=user_rating)

@app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    rating_form = RatingForm()
    if comment_form.validate_on_submit():
        db.session.add(Comment(content=comment_form.comment.data, post_id = post.id, author_id=current_user.id))
        db.session.commit()
        flash('Your comment has beesn added to the post', 'success')
        return redirect(f'/post/{post.id}')
    
    comments = Comment.query.filter(Comment.post_id == post.id)
    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, rating_form=rating_form)

@app.route('/post/<int:post_id>/rate', methods=['GET', 'POST'])
@login_required
def rate_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    comments = Comment.query.filter(Comment.post_id == post.id)

    rating_form = RatingForm()
    if rating_form.validate_on_submit():
        
        #Check if user has already given this post a rating
        old_rating = Rating.query.filter_by(rater_id=current_user.id, post_id=post.id).first()
        if old_rating:
            old_rating.rating = rating_form.rating.data
        else:
            db.session.add(Rating(rating=rating_form.rating.data, rater_id=current_user.id, post_id = post.id))
        db.session.commit()
        flash('Your rating has been added to the post', 'success')
        return redirect(f'/post/{post.id}')
    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, rating_form=rating_form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        return redirect(url_for('posts', search_form=searched))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='LT | Register', form=form, search_form=search_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email address or password.')
    
    search_form = SearchForm(request.form)
    if request.method == 'POST':
        searched = search_form.search.data
        return redirect(url_for('posts', search_form = searched))
    return render_template('login.html', title='LT | Login', form=form, search_form=search_form)

#This page needs testing!
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
