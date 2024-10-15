from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, AddBookForm, AddUserForm
from models import db, User, Book
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    books = Book.query.all()
    if current_user.is_admin:
        users_link = url_for('users')
    else:
        users_link = None
    return render_template('index.html', books=books, users_link=users_link, is_admin=current_user.is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
@login_required
def user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/create_db')
def create_db():
    db.create_all()
    return "Database created!"


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Only administrators can add users.')
        return redirect(url_for('index'))

    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, is_admin=form.is_admin.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('index'))

    return render_template('add_user.html', form=form)

@app.route('/add_regular_user')
def add_regular_user():
    hashed_password = bcrypt.generate_password_hash('userpassword').decode('utf-8')
    new_user = User(username='normaluser', password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    return "Regular user added!"



@app.route('/add_user_form', methods=['GET', 'POST'])
def add_user_form():
    form = AddUserForm()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')
        return redirect(url_for('index'))
    return render_template('add_user.html', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('index'))  
    return render_template('add_book.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)
