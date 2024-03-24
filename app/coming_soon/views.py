from app import mysql
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from pytz import timezone

coming_soon = Blueprint('coming_soon', __name__)
@coming_soon.route('/coming_soon')
def comingsoon():
    movieid = request.args.get('movieid')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        WITH cte_star AS (
            SELECT 
                s.movieid,
                GROUP_CONCAT(a.actor_name SEPARATOR ', ') AS starring
            FROM 
                starring s
                LEFT JOIN actors a ON a.actorid = s.actorid
            WHERE 
                s.latest_version = 1
            GROUP BY 
                s.movieid
        )
        SELECT 
            m.*, 
            m.runtime_hour * 60 + runtime_minute AS runtime,
            g.genre_name,
            r.rating_code,
            r.color,
            cs.starring
        FROM 
            movies m
            LEFT JOIN genre g ON g.genreid = m.genreid
            LEFT JOIN ratings r ON r.ratingid = m.ratingid
            LEFT JOIN cte_star AS cs ON cs.movieid = m.movieid
        WHERE 
            m.start_date BETWEEN %s AND %s; 
        """
    # calculate today and next 30 days 
    today = datetime.now(timezone('Pacific/Auckland'))
    today7 = today + timedelta(days=7)
    today30 = today + timedelta(days=30)

    parameters = (today7.strftime('%Y-%m-%d'), today30.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters)
    movies = cursor.fetchall()
    return render_template('coming_soon.html', movies=movies, movieid=movieid)

@coming_soon.route('/home/coming_soon')
def home_comingsoon():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        WITH cte_star AS (
            SELECT 
                s.movieid,
                GROUP_CONCAT(a.actor_name SEPARATOR ', ') AS starring
            FROM 
                starring s
                LEFT JOIN actors a ON a.actorid = s.actorid
            WHERE 
                s.latest_version = 1
            GROUP BY 
                s.movieid
        )
        SELECT 
            m.*, 
            m.runtime_hour * 60 + runtime_minute AS runtime,
            g.genre_name,
            r.rating_code,
            r.color,
            cs.starring
        FROM 
            movies m
            LEFT JOIN genre g ON g.genreid = m.genreid
            LEFT JOIN ratings r ON r.ratingid = m.ratingid
            LEFT JOIN cte_star AS cs ON cs.movieid = m.movieid
        WHERE 
            m.start_date BETWEEN %s AND %s; 
        """
    # calculate today and next 30 days 
    today = datetime.now(timezone('Pacific/Auckland'))
    today7 = today + timedelta(days=7)
    today30 = today + timedelta(days=30)

    parameters = (today7.strftime('%Y-%m-%d'), today30.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters)
    movies = cursor.fetchall()
    return render_template('home_coming_soon.html', movies=movies)