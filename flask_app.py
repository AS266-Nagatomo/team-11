import os
import datetime
import sqlite3
from flask import Flask,  redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
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

class anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    datetime = db.Column(db.DateTime)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class nobel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    datetime = db.Column(db.DateTime)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),)
    reputation = db.Column(db.String(50), unique=True)
    datetime = db.Column(db.DateTime)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)



@login_maneger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_maneger.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username= request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form)
        username= request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is not None and  check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    print("aaa")
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db2 = conn.cursor()
    if request.method == "POST":
        type = request.form.get("type")
        title = request.form.get("title")
        reputation= request.form.get("reputation")
        point = request.form.get("point")
        submit = request.form.get("submit")
        time = datetime.date.today()
        Anime = anime()
        Movie = movie()
        Nobel = nobel()

        if type == "movie":
            if submit == "delete":
                db2.execute("DELETE FROM  movie WHERE title = ?", title)
            if len(title) == 0 :
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                    """db2.execute("INSERT INTO  movie (title, reputation, point, datetime) VALUES(?, ?, ?, ?)", (title, reputation, point, time))"""
                    Movie.title = title
                    Movie.reputation = reputation
                    Movie.point = point
                    Movie.datetime = time
                    db.session.add(Movie)
                    db.session.commit()
        elif type == "nobel":
            if submit == "delete":
                db2.execute("DELETE FROM  nobel WHERE title = ?", title)
            if len(title) == 0:
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                   db2.execute("INSERT INTO  nobel (title, reputation, point, datetime) VALUES(?, ?, ? ,?)", (title, reputation, point, time))
        elif type == "anime":
            if submit == "delete":
                db2.execute("DELETE FROM  anime WHERE title = ?", title)
            if len(title) == 0:
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                   db2.execute("INSERT INTO  anime (title, reputation, point, datetime) VALUES(?, ?, ?, ?)", (title, reputation, point, time))
        conn.commit()

        #sort
        sort = request.form.get("sort")
        sort_genre = request.form.get("sort_genre")

        if sort == "sort_title":
            if sort_genre == "sort_Movie":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie ORDER BY title ")
                animes = db2.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime ORDER BY title")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db2.execute("SELECT * FROM nobel order by title")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        elif sort == "sort_point":
            if sort_genre == "sort_Movie":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie order by point desc")
                animes = db2.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime order by point desc")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db2.execute("SELECT * FROM nobel order by point desc")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        elif sort == "sort_when":
            if sort_genre == "sort_Movie":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie order by datetime")
                animes = db2.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db2.execute("SELECT * FROM nobel")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime order by datetime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db2.execute("SELECT * FROM nobel order by datetime")
                movies = db2.execute("SELECT * FROM movie ")
                animes = db2.execute("SELECT * FROM anime ")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        return redirect("/")
    else:
        nobels = db2.execute("SELECT * FROM nobel").fetchall()
        movies = db2.execute("SELECT * FROM movie").fetchall()
        animes = db2.execute("SELECT * FROM anime").fetchall()
        conn.commit()
        return render_template("index.html", nobels=nobels, animes=animes, movies=movies)

@app.route("/Nobel", methods=["GET", "POST"])
@login_required
def nobel():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db2 = conn.cursor()
    if request.method == "GET":
        nobels = db2.execute("SELECT * FROM nobel")
        return render_template("nobel.html", nobels=nobels)
    else:
         #sort
        sort = request.form.get("sort_nobel")
        if sort == "sort_title_nobel":
            nobels = db2.execute("SELECT * FROM nobel order by title")
            return render_template("nobel.html", nobels=nobels)
        elif sort == "sort_point_nobel":
            nobels = db2.execute("SELECT * FROM nobel order by point desc")
            return render_template("nobel.html", nobels=nobels)
        elif sort == "sort_when_nobel":
            nobels = db2.execute("SELECT * FROM nobel order by datetime")
            return render_template("nobel.html", nobels=nobels)
        return redirect("/Nobel")

@app.route("/Anime", methods=["GET", "POST"])
@login_required
def anime():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db2 = conn.cursor()
    if request.method == "GET":
        animes = db2.execute("SELECT * FROM anime")
        return render_template("anime.html", animes=animes)
    else:
         #sort
        sort = request.form.get("sort_nobel")
        if sort == "sort_title_nobel":
            animes = db2.execute("SELECT * FROM anime order by title")
            return render_template("nobel.html", animes=animes)
        elif sort == "sort_point_nobel":
            animes = db2.execute("SELECT * FROM anime order by point desc")
            return render_template("nobel.html", animes=animes)
        elif sort == "sort_when_nobel":
            animes = db2.execute("SELECT * FROM anime order by datetime")
            return render_template("nobel.html", animes=animes)
        return redirect("/Anime")

@app.route("/Movie", methods=["GET", "POST"])
@login_required
def movie():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db2 = conn.cursor()
    if request.method == "GET":
        movies = db2.execute("SELECT * FROM movie")
        return render_template("movie.html", movies=movies)
    else:
         #sort
        sort = request.form.get("sort_movie")
        if sort == "sort_title_movie":
            movies = db2.execute("SELECT * FROM movie order by title")
            return render_template("movie.html", movies=movies)
        elif sort == "sort_point_movie":
            movies = db2.execute("SELECT * FROM movie order by point desc")
            return render_template("movie.html", movies=movies)
        elif sort == "sort_when_movie":
            movies = db2.execute("SELECT * FROM movie order by datetime")
            return render_template("movie.html", movies=movies)
        return redirect("/Movie")


