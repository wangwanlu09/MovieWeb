from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

home = Blueprint('home', __name__)

@home.route('/')
def homepage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
            select 
                m.*, m.runtime_hour * 60 + runtime_minute as runtime
                ,g.genre_name, r.rating_code, r.color  
            from movies m
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            where m.movieid in (
                select distinct movieid
                from sessions 
                where session_date between %s and %s
            );
        """
    # calculate today and next 6 days 
    today = datetime.now(timezone('Pacific/Auckland'))
    date7 = today + timedelta(days=6)
    parameters = (today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters)
    movies = cursor.fetchall()
    return render_template('home.html', movies=movies)


@home.route('/logout') #clear the infomation in session when logout
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('accountid', None)
    session.pop('booking_url', None)
    session.pop('url', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('home.homepage'))

@home.route('/movies')
def movies():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
            with cte_star AS (
            select s.movieid 
                ,GROUP_CONCAT(a.actor_name SEPARATOR ', ') as starring
            from starring s
            left join actors a on a.actorid = s.actorid
            where s.latest_version = 1
            group by s.movieid
            )
            select 
                m.*, m.runtime_hour * 60 + runtime_minute as runtime
                ,g.genre_name
                ,r.rating_code, r.color 
                ,cs.starring 
            from movies m
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            left join cte_star as cs on cs.movieid = m.movieid
            where m.movieid in (
                select distinct movieid
                from sessions 
                where session_date between %s and %s
            );
        """
    # calculate today and next 6 days 
    today = datetime.now(timezone('Pacific/Auckland'))
    date7 = today + timedelta(days=6)
    parameters = (today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters)
    movies = cursor.fetchall()
    return render_template('movies_home.html', movies = movies)

@home.route('/contactus')
def contactus():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from company where latest_version = 1;")
    contact = cursor.fetchone()
    return render_template('Contact.html', contact=contact)

@home.route('/contact/sendmessage', methods=['POST'])
def send_message():
    # fullname = request.form['fullname']
    # email = request.form['email']
    # message = request.form['message']
    # now = datetime.now(timezone('Pacific/Auckland'))
    
    # current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute("INSERT INTO contact_message (fullname, email, message, send_datetime) VALUES (%s, %s, %s, %s)", (fullname, email, message, current_timestamp))
    # mysql.connection.commit()

    flash("Message sent successfully!", "success")
    return redirect(url_for('home.contactus'))