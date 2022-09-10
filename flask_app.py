
# A very simple Flask Hello World app for you to get started with...
import os
import datetime
import sqlite3
from flask import Flask,  redirect, render_template, request


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
dbname = 'reading_record.db'

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    print("aaa")
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db = conn.cursor()
    if request.method == "POST":
        type = request.form.get("type")
        title = request.form.get("title")
        reputation= request.form.get("reputation")
        point = request.form.get("point")
        submit = request.form.get("submit")
        time = datetime.date.today()

        if type == "movie":
            if submit == "delete":
                db.execute("DELETE FROM  movie WHERE title = ?", title)
            if len(title) == 0 :
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                    db.execute("INSERT INTO  movie (title, reputation, point, datetime) VALUES(?, ?, ?, ?)", (title, reputation, point, time))
        elif type == "nobel":
            if submit == "delete":
                db.execute("DELETE FROM  nobel WHERE title = ?", title)
            if len(title) == 0:
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                   db.execute("INSERT INTO  nobel (title, reputation, point, datetime) VALUES(?, ?, ? ,?)", (title, reputation, point, time))
        elif type == "anime":
            if submit == "delete":
                db.execute("DELETE FROM  anime WHERE title = ?", title)
            if len(title) == 0:
                return redirect("/")
            if len(point) == 0:
                return redirect("/")
            else:
                if submit == "add":
                   db.execute("INSERT INTO  anime (title, reputation, point, datetime) VALUES(?, ?, ?, ?)", (title, reputation, point, time))
        conn.commit()

        #sort
        sort = request.form.get("sort")
        sort_genre = request.form.get("sort_genre")

        if sort == "sort_title":
            if sort_genre == "sort_Movie":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie ORDER BY title ")
                animes = db.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime ORDER BY title")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db.execute("SELECT * FROM nobel order by title")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        elif sort == "sort_point":
            if sort_genre == "sort_Movie":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie order by point desc")
                animes = db.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime order by point desc")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db.execute("SELECT * FROM nobel order by point desc")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        elif sort == "sort_when":
            if sort_genre == "sort_Movie":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie order by datetime")
                animes = db.execute("SELECT * FROM anime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Anime":
                nobels = db.execute("SELECT * FROM nobel")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime order by datetime")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
            if sort_genre == "sort_Nobel":
                nobels = db.execute("SELECT * FROM nobel order by datetime")
                movies = db.execute("SELECT * FROM movie ")
                animes = db.execute("SELECT * FROM anime ")
                return render_template("index.html", nobels=nobels, animes=animes, movies=movies)
        return redirect("/")
    else:
        nobels = db.execute("SELECT * FROM nobel").fetchall()
        movies = db.execute("SELECT * FROM movie").fetchall()
        animes = db.execute("SELECT * FROM anime").fetchall()
        conn.commit()
        return render_template("index.html", nobels=nobels, animes=animes, movies=movies)

@app.route("/Nobel", methods=["GET", "POST"])
def nobel():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db = conn.cursor()
    if request.method == "GET":
        nobels = db.execute("SELECT * FROM nobel")
        return render_template("nobel.html", nobels=nobels)
    else:
         #sort
        sort = request.form.get("sort_nobel")
        if sort == "sort_title_nobel":
            nobels = db.execute("SELECT * FROM nobel order by title")
            return render_template("nobel.html", nobels=nobels)
        elif sort == "sort_point_nobel":
            nobels = db.execute("SELECT * FROM nobel order by point desc")
            return render_template("nobel.html", nobels=nobels)
        elif sort == "sort_when_nobel":
            nobels = db.execute("SELECT * FROM nobel order by datetime")
            return render_template("nobel.html", nobels=nobels)
        return redirect("/Nobel")

@app.route("/Anime", methods=["GET", "POST"])
def anime():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db = conn.cursor()
    if request.method == "GET":
        animes = db.execute("SELECT * FROM anime")
        return render_template("anime.html", animes=animes)
    else:
         #sort
        sort = request.form.get("sort_nobel")
        if sort == "sort_title_nobel":
            animes = db.execute("SELECT * FROM anime order by title")
            return render_template("nobel.html", animes=animes)
        elif sort == "sort_point_nobel":
            animes = db.execute("SELECT * FROM anime order by point desc")
            return render_template("nobel.html", animes=animes)
        elif sort == "sort_when_nobel":
            animes = db.execute("SELECT * FROM anime order by datetime")
            return render_template("nobel.html", animes=animes)
        return redirect("/Anime")

@app.route("/Movie", methods=["GET", "POST"])
def movie():
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    db = conn.cursor()
    if request.method == "GET":
        movies = db.execute("SELECT * FROM movie")
        return render_template("movie.html", movies=movies)
    else:
         #sort
        sort = request.form.get("sort_movie")
        if sort == "sort_title_movie":
            movies = db.execute("SELECT * FROM movie order by title")
            return render_template("movie.html", movies=movies)
        elif sort == "sort_point_movie":
            movies = db.execute("SELECT * FROM movie order by point desc")
            return render_template("movie.html", movies=movies)
        elif sort == "sort_when_movie":
            movies = db.execute("SELECT * FROM movie order by datetime")
            return render_template("movie.html", movies=movies)
        return redirect("/Movie")


