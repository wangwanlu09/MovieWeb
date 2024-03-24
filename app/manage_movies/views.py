from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

managemovies = Blueprint('managemovies', __name__)

@managemovies.route('/manage/movies')
def movies_view():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        today = datetime.now(timezone('Pacific/Auckland'))
        current_timestamp = today.strftime("%Y-%m-%d %H:%M:%S")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # redirected from manage schedule

        if 'movieid' in request.args.keys():
            movieid = request.args.get('movieid')
            sql = """
            with cte_star AS (
                select s.movieid 
                    ,GROUP_CONCAT(a.actor_name SEPARATOR ', ') as starring
                from starring s
                left join actors a on a.actorid = s.actorid
                where s.latest_version = 1
                group by s.movieid
            )
            ,cte_sessions as (
                select s.movieid, count(s.sessionid) as schedules
                from sessions s
                left join sessiontime t on t.sessiontime_id = s.sessiontime_id
                
                group by s.movieid
            )
            select m.* 
                ,g.genre_name
                ,r.rating_code
                ,cs.starring
                ,case when s.schedules is null then 0 else s.schedules end as schedules
            from movies m
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            left join cte_star cs on cs.movieid = m.movieid
            left join cte_sessions s on s.movieid = m.movieid
            where m.movieid = %s
            """
            cursor.execute(sql, (movieid, ))
        else:
            sql = """
            with cte_star AS (
                select s.movieid 
                    ,GROUP_CONCAT(a.actor_name SEPARATOR ', ') as starring
                from starring s
                left join actors a on a.actorid = s.actorid
                where s.latest_version = 1
                group by s.movieid
            )
            ,cte_sessions as (
                select s.movieid, count(s.sessionid) as schedules
                from sessions s
                left join sessiontime t on t.sessiontime_id = s.sessiontime_id
               
                group by s.movieid
            )
            select m.* 
                ,g.genre_name
                ,r.rating_code
                ,cs.starring
                ,case when s.schedules is null then 0 else s.schedules end as schedules
            from movies m
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            left join cte_star cs on cs.movieid = m.movieid
            left join cte_sessions s on s.movieid = m.movieid
            """
            cursor.execute(sql)

        movies = cursor.fetchall()
        return render_template('managemovies.html', movies = movies)
    else:
        return redirect(url_for('staff_login.stafflogin'))

@managemovies.route('/add/newmovie')
def movie_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from actors order by actor_name;")        
        actors = cursor.fetchall()
        cursor.execute("select * from ratings;")  
        ratings = cursor.fetchall()
        cursor.execute("select * from genre;")  
        genre = cursor.fetchall()
        return render_template('movie_add.html', actors = actors, ratings = ratings, genre = genre)
    else:
        flash("Plase login as manager or admin to add new movie", "warning")
        return redirect(url_for('staff_login.stafflogin'))

# update new movie info to databse
@managemovies.route('/add_db/newmovie', methods=['POST', 'GET'])
def movie_add_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        title = request.form['newName']
        release_date = request.form['newDate']
        descriptions = request.form['newDescription']
        runtime_hour = request.form['newRuntimeHours']
        runtime_minute = request.form['newRuntimeMinutes']
        genreid = request.form['newGenre']
        ratingid = request.form['newRating']
        image_url = request.form['newImage']
        startdate = request.form['startdate']
        starring = request.form.getlist('starrings')
        parameters = (title, release_date, descriptions, runtime_hour, runtime_minute, genreid, ratingid, image_url, startdate)
        sql = """
            INSERT INTO movies (title, release_date, descriptions, runtime_hour, runtime_minute, genreid, ratingid, image_url, start_date)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # create new movie in movies table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, parameters)

        # create new movie-actor pairs in starring
        movieid = cursor.lastrowid
        sql_star = """
            INSERT INTO starring (movieid, actorid)
            VALUES 
            (%s, %s)
            """
        for actor in starring:
            cursor.execute(sql_star, (movieid, actor))
        
        # commit changes to movies and starring
        mysql.connection.commit()

        flash(f"Movie {title} is now added", "success")
        return redirect(url_for('managemovies.movies_view'))
    else:
        flash("Plase login as manager or admin to add new movie", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@managemovies.route('/edit/movie', methods=['POST', 'GET'])
def movie_edit():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        movieid = request.args.get("movieid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            select m.* 
                ,g.genre_name
                ,r.rating_code
            from movies m
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            where m.movieid = %s
        """
        parameters = (movieid, )
        cursor.execute(sql, parameters)
        movie = cursor.fetchone()
        cursor.execute("select * from actors order by actor_name;")        
        actors = cursor.fetchall()
        cursor.execute("select * from ratings;")  
        ratings = cursor.fetchall()
        cursor.execute("select * from genre;")  
        genre = cursor.fetchall()
        cursor.execute("select distinct actorid from starring where movieid = %s and latest_version = 1;", (movieid, )) 
        stars = cursor.fetchall()
        starring = [ sub['actorid'] for sub in stars ]
        return render_template("movie_edit.html", movie = movie, actors = actors, ratings = ratings, genre = genre, starring =  starring)
    else:
        flash("Plase login as manager or admin to edit movies", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@managemovies.route('/update/movie', methods=['POST', 'GET'])
def movie_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        movieid = request.form['movieid']
        title = request.form['title']
        release_date = request.form['release']
        descriptions = request.form['descriptions']
        runtime_hour = request.form['hour']
        runtime_minute = request.form['minute']
        genreid = request.form['genre']
        ratingid = request.form['rating']
        image_url = request.form['image']
        startdate = request.form['startdate']
        starring = request.form.getlist('starrings')

        parameters_movie = (title, release_date, startdate, descriptions, runtime_hour, runtime_minute, genreid, ratingid, image_url, movieid)
        sql_movie = """
                UPDATE movies
                SET title = %s, release_date = %s, start_date = %s, descriptions = %s, runtime_hour = %s, runtime_minute = %s, genreid = %s, ratingid = %s, image_url = %s
                WHERE movieid = %s
                ;
            """
        # update movies table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_movie, parameters_movie)

        # update starring table

        # 1. update previous movie id in starring table latest version = 0 (false)
        sql_false = """
                UPDATE starring
                SET latest_version = 0
                WHERE movieid = %s;
            """
        cursor.execute(sql_false, (movieid,))
        # 2. insert new starring movie-actor pairs to starring table
        sql_starring = """
                INSERT INTO starring (movieid, actorid)
                VALUES
                (%s, %s)
            """
        for actorid in starring:
            cursor.execute(sql_starring, (movieid, actorid))

        # commit changes
        mysql.connection.commit()

        flash(f"Movie - id {movieid} title {title} is now updated", "success")
        return redirect(url_for('managemovies.movies_view'))
    else:
        flash("Plase login as manager or admin to edit movies", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@managemovies.route('/delete/movie', methods=['POST', 'GET'])
def movie_delete():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        movieid = request.args.get('movieid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        today = datetime.now(timezone('Pacific/Auckland'))
        current_timestamp = today.strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            select s.movieid, count(s.sessionid) as schedules
            from sessions s
            left join sessiontime t on t.sessiontime_id = s.sessiontime_id
            where timestamp(s.session_date, t.sessiontime) > %s
            and s.movieid = %s
            group by s.movieid
            """
        cursor.execute(sql, (current_timestamp, movieid))
        countsessions = cursor.fetchone()
        if countsessions:
            flash("Please delete sessions scheduled for this moive before deleting the movie", "warning")
            return redirect(url_for('managemovies.movies_view'))
        else:
            cursor.execute("DELETE FROM movies WHERE movieid = %s;", (movieid,))
            mysql.connection.commit()
            flash(f"Movie - id {movieid} is now deleted", "success")
            return redirect(url_for('managemovies.movies_view'))
    else:
        flash("Plase login as manager or admin to delete movies", "warning")
        return redirect(url_for('staff_login.stafflogin'))
