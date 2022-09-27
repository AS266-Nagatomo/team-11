import os
from flask import Flask,  redirect, render_template, request, session, jsonify
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
    reputation = db.Column(db.String(50))
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)
    consent = db.Column(db.Boolean)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50))
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)
    consent = db.Column(db.Boolean)

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50))
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    api_id = db.Column(db.Integer)
    consent = db.Column(db.Boolean)




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
        username= request.form.get('user-name')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None and  check_password_hash(user.password, password):
            login_user(user)
            return redirect('/Mypage')
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
    return render_template("index.html")


@app.route("/api/ranking", methods=["GET", "POST"])
def get_ranking():
    books = [tuple(row) for row in db.session.query(Book.api_id, sa.func.sum(Book.point)).filter(Book.consent==True).group_by(Book.api_id).order_by(sa.desc(sa.func.sum(Book.point))).limit(5)]
    animes = [tuple(row) for row in db.session.query(Anime.api_id, sa.func.sum(Anime.point)).filter(Anime.consent==True).group_by(Anime.api_id).order_by(sa.desc(sa.func.sum(Anime.point))).limit(5)]
    movies = [tuple(row) for row in db.session.query(Movie.api_id, sa.func.sum(Movie.point)).filter(Movie.consent==True).group_by(Movie.api_id).order_by(sa.desc(sa.func.sum(Movie.point))).limit(5)]
    return jsonify(dict(anime=animes, book=books, movie=movies))


@app.route("/Mypage", methods=["GET", "POST"])
@login_required
def get_mypage():
    if request.method == "POST":
        genre = request.form.get("genre") 
        title_list = request.form.get("title").split("@")
        title = title_list[0]
        reputation= request.form.get("reputation")
        point = request.form.get("point")
        consent = request.form.get("consent", "false")=="true"
        api_id = title_list[1]

        anime = Anime()
        movie = Movie()
        book = Book()

        if genre == "movie":
            movie.title = title
            movie.reputation = reputation
            movie.user_id = current_user.id
            movie.point = point
            movie.api_id = api_id
            movie.consent = consent
            db.session.add(movie)
            db.session.commit()
        elif genre == "book":
            book.title = title
            book.reputation = reputation
            book.point = point
            book.user_id = current_user.id
            book.api_id = api_id
            book.consent = consent
            db.session.add(book)
            db.session.commit()
        elif genre == "anime":
            anime.title = title
            anime.reputation = reputation
            anime.point = point
            anime.user_id = current_user.id
            anime.api_id = api_id
            anime.consent = consent
            db.session.add(anime)
            db.session.commit()

    else:
        return render_template("Mypage.html")
    return render_template("Mypage.html")



@app.route("/Book", methods=["GET", "POST"])
@login_required
def get_books():
    if request.method == "GET":
        books = db.session.query(Book).filter(Book.user_id==current_user.id).all()
        return render_template("Book.html", books=books)
    else:
        genre = request.form.get("genre")
        if genre == "descend":
            books = db.session.query(Book).filter(Book.user_id==current_user.id).order_by(Book.point.desc()).all()
            return render_template("Book.html", books=books)
        elif genre == "acsend":
            books = db.session.query(Book).filter(Book.user_id==current_user.id).order_by(Book.point).all()
            return render_template("Book.html", books=books)
        elif genre == "alpha":
            books = db.session.query(Book).filter(Book.user_id==current_user.id).order_by(Book.title).all()
            return render_template("Book.html", books=books)

        id= request.form.get("target")
        db.session.query(Book).filter(Book.user_id==current_user.id, Book.id==id).delete()
        db.session.commit()
    return redirect("/Book")


@app.route("/Anime", methods=["GET", "POST"])
@login_required
def get_animes():
    if request.method == "GET":
        animes = db.session.query(Anime).filter(Anime.user_id==current_user.id).all()
        return render_template("anime.html", animes=animes)
    else:
        genre = request.form.get("genre")
        if genre == "descend":
            animes = db.session.query(Anime).filter(Anime.user_id==current_user.id).order_by(Anime.point.desc()).all()
            print("pop")
            return render_template("anime.html", animes=animes)
        elif genre == "acsend":
            animes = db.session.query(Anime).filter(Anime.user_id==current_user.id).order_by(Anime.point).all()
            return render_template("anime.html", animes=animes)
        elif genre == "alpha":
            animes = db.session.query(Anime).filter(Anime.user_id==current_user.id).order_by(Anime.title).all()
            return render_template("anime.html", animes=animes)

        id= request.form.get("target")
        db.session.query(Anime).filter(Anime.user_id==current_user.id, Anime.id==id).delete()
        db.session.commit()
    return redirect("/Anime")


@app.route("/Movie", methods=["GET", "POST"])
@login_required
def get_movies():
    if request.method == "GET":
        movies = db.session.query(Movie).filter(Movie.user_id==current_user.id).all()
        return render_template("movie.html", movies=movies)
    else:
        genre = request.form.get("genre")
        if genre == "descend":
            movies = db.session.query(Movie).filter(Movie.user_id==current_user.id).order_by(Movie.point.desc()).all()
            return render_template("movie.html", movies=movies)
        elif genre == "acsend":
            movies = db.session.query(Movie).filter(Movie.user_id==current_user.id).order_by(Movie.point).all()
            return render_template("movie.html", movies=movies)
        elif genre == "alpha":
            movies = db.session.query(Movie).filter(Movie.user_id==current_user.id).order_by(Movie.title).all()
            return render_template("movie.html", movies=movies)

        id= request.form.get("target")
        db.session.query(Movie).filter(Movie.user_id==current_user.id, Movie.id==id).delete()
        db.session.commit()
    return redirect("/Movie")
