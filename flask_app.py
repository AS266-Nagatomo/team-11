import os
from flask import Flask,  redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy 
import sqlalchemy as sa
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/',)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)
dbname = 'user.db'


login_maneger = LoginManager()
login_maneger.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12), unique=True)

class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)




@login_maneger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_maneger.unauthorized_handler
def unauthorized():
    return redirect('/sign-in')


@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username= request.form.get('user-name')
        password = request.form.get('password')
        repassword = request.form.get('re:password')
        if password != repassword:
            return redirect("/sign-up")
        user = User.query.filter_by(username=username).first()

        if password != repassword:
            return redirect('/sign-up')
        if user is None :
            user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            return redirect('/sign-in')
        else:
            return redirect('/sign-in')
    else:
        return render_template('sign-up.html')

@app.route('/sign-in', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        username= request.form.get('user-name')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None and  check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        return redirect('/sign-up')
    else:
        return render_template('/sign-in.html')


@app.route('/sign-out')
@login_required
def logout():
    logout_user()
    return redirect('/sign-in')


@app.route("/", methods=["GET", "POST"])
def get_index():
    """books = db.session.query(Book).distinct(Book.point).limit(5).all()
    animes = db.session.query(Anime).distinct(Anime.point).limit(5).all()
    animes = db.session.query(Anime.id, sa.func.sum(Anime.point)).group_by(Anime.id).limit(5).all()
    print(animes)
    movies = db.session.query(Movie).distinct(Movie.point).limit(5).all()"""
    animes = db.session.query(Anime.id, sa.func.sum(Anime.point)).group_by(Anime.id).limit(5).all()
    print(animes)

    return render_template("index.html",animes=animes)


@app.route("/Mypage", methods=["GET", "POST"])
@login_required
def get_mypage():
    if request.method == "POST":
        genre = request.form.get("genre")
        title = request.form.get("title")
        reputation= request.form.get("reputation")
        point = request.form.get("point")
        api_id = request.form.get("api_id")
        anime = Anime()
        movie = Movie()
        book = Book()

        if genre == "movie":
            movie.title = title
            movie.reputation = reputation
            movie.user_id = current_user.id
            movie.point = point
            movie.api_id = api_id
            db.session.add(movie)
            db.session.commit()
        elif genre == "book":
            book.title = title
            book.reputation = reputation
            book.point = point
            book.user_id = current_user.id
            book.api_id = api_id
            db.session.add(book)
            db.session.commit()
        elif genre == "anime":
            anime.title = title
            anime.reputation = reputation
            anime.point = point
            anime.user_id = current_user.id
            anime.api_id = api_id
            db.session.add(anime)
            db.session.commit()
    else:
        return render_template("Mypage.html")
    return render_template("Mypage.html")



@app.route("/Book", methods=["GET", "POST"])
@login_required
def get_books():
    books = db.session.query(Book).filter(Book.user_id==current_user.id).all()
    if request.method == "GET":
        return render_template("Book.html", books=books)
    return render_template("Book.html")


@app.route("/Anime", methods=["GET", "POST"])
@login_required
def get_animes():
    animes = db.session.query(Anime).filter(Anime.user_id==current_user.id).all()
    if request.method == "GET":
        return render_template("anime.html", animes=animes)
    return render_template("anime.html")


@app.route("/Movie", methods=["GET", "POST"])
@login_required
def get_movies():
    movies = db.session.query(Movie).filter(Movie.user_id==current_user.id).all()
    if request.method == "GET":
        return render_template("movie.html", movies=movies)
    return render_template("movie.html")
