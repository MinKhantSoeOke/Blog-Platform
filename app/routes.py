from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, ChangePasswordForm
from app.models import User, Post, Comment, Like
from flask_login import login_user, current_user, logout_user, login_required
from emails import reset_password_email

# Displays all posts in descending order of the date posted
@app.route("/", methods=['GET'])
@app.route("/home",  methods=['GET'])
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)

# Handles user registration with form validation, password hashing, and user creation
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Handles user login with form validation, password verification, and user session management
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            password = User.generate_random_password()
            print(password)
            reset_password_email(user.username, user.email, password)
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = password
            db.session.commit()
            flash ('Password sent successfully to your email.', 'success')
            return redirect('/login')
        else:
            flash('There is no user with this email', 'danger')
    return render_template('reset_password.html')

# Logs the user out
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Allows users to update their account details
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(change_password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
        else:
            flash('Old password is incorrect', 'danger')
        return redirect(url_for('account'))

    return render_template('account.html', title='Account', form=form, change_password_form=change_password_form)

# Allows logged-in users to create new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

# Displays a single post and its comments
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    return render_template('post.html', title=post.title, post=post, form=form)

# Allows logged-in users to update their own posts
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)

# Allows logged-in users to delete their own posts
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# Allows logged-in users to comment on posts
@app.route("/post/<int:post_id>/comment", methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_name=current_user.username, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return redirect(url_for('post', post_id=post.id))

# Allows logged-in users to like or unlike posts
@app.route("/post/<int:post_id>/like", methods=['GET','POST'])
@login_required
def like_post(post_id):
    if request.method == 'POST':
        post = Post.query.get_or_404(post_id)
        like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if like:
            db.session.delete(like)
        else:
            like = Like(user_id=current_user.id, post_id=post.id)
            db.session.add(like)
        db.session.commit()
        return redirect(request.referrer or url_for('post', post_id=post.id))
       