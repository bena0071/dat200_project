from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, EmptyForm, CommentForm
from app.models import User, Post, Comment
from sqlalchemy import func


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now posted!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], True)
    if posts.has_next is True:
        next_url = url_for('index', page=posts.next_num)
    else:
        next_url = None
    if posts.has_prev is True:
        prev_url = url_for('index', page=posts.prev_num)
    else:
        prev_url = None
    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], True)
    if posts.has_next:
        next_url = url_for('user', username=username, page=posts.next_num)
    else:
        next_url = None
    if posts.has_prev:
        prev_url = url_for('user', username=username, page=posts.prev_num)
    else:
        prev_url = None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(func.lower(User.username).asc()).paginate(
        page, app.config['ACCOUNTS_PER_PAGE'], True)
    if users.has_next:
        next_url = url_for('explore', page=users.next_num)
    else:
        next_url = None
    if users.has_prev:
        prev_url = url_for('explore', page=users.prev_num)
    else:
        prev_url = None
    return render_template('explore.html', title='People', users=users.items, next_url=next_url, prev_url=prev_url)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id=None):
    postid = request.args.get('post', post_id)
    post = Post.query.filter_by(id=postid).first_or_404()
    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data,
                          author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment was successful!')
        return redirect(url_for('post', post_id=post.id, page=page))
    comments = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, app.config['COMMENTS_PER_PAGE'], True)
    if comments.has_next:
        next_url = url_for('post', post_id=post.id, page=comments.next_num)
    else:
        next_url = None
    if comments.has_prev:
        prev_url = url_for('post', post_id=post.id, page=comments.prev_num)
    else:
        prev_url = None
    return render_template('comments.html', title='Write a comment', post=post, form=form, comments=comments.items, next_url=next_url, prev_url=prev_url)
