
from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session,request,jsonify,abort,flash
import datetime,json
from datetime import date, datetime, timedelta
import MySQLdb.cursors
from pytz import timezone

movie_schedule = Blueprint('movie_schedule', __name__)

@movie_schedule.route('/manage/schedules',methods=['GET'])     # This route is showing all the sessions and times in a combined page
def manage_schedules():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute("SELECT MAX(session_date) AS last_date FROM sessions;")
        # last_date =list(cursor.fetchall())  # the pop up has a date for user to select and the last day is for the last day in dates table. 
        today = datetime.now(timezone('Pacific/Auckland'))
        today30 = today + timedelta(days=30)
        last_date = today30
        current_timestamp = today.strftime("%Y-%m-%d %H:%M:%S")
        current_date = today.strftime("%Y-%m-%d")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM movies;")
        movies =list(cursor.fetchall())  # get movieid and movie title for displaying
        
        # redirected from manage movies
        if 'movieid' in request.args.keys():
            movieid = request.args.get('movieid')
            sql = """
            with cte_seats as (
                select s.sessionid, count(bs.seatid) as booked_seats
                from bookings b
                left join sessions s on s.sessionid = b.sessionid
                left join booking_seats bs on bs.bookingid = b.bookingid
                -- where s.session_date >= current_date()
                group by s.sessionid
            )
            ,cte_cinema as (
                select c.cinemaid, c.name, count(s.seatid) as cinema_seats
                from cinemas c
                left join seats s on s.cinemaid = c.cinemaid
                group by c.cinemaid, c.name
            )
            SELECT
                m.title,
                m.movieid,
                DATE_FORMAT(s.session_date, '%%d/%%m/%%Y') AS sd,
                s.sessionid,
                c.name,
                d.weekday_name,
                TIME_FORMAT(t.sessiontime, '%%h:%%i %%p') AS sessiontime_12hrs
                ,case when cs.booked_seats is null then 0 else cs.booked_seats end as booked_seats
                ,c.cinema_seats
                ,case when cs.booked_seats is null then c.cinema_seats else c.cinema_seats - cs.booked_seats end as available_seats
                ,case when timestamp(s.session_date, t.sessiontime) > %s then 1 else 0 end as is_current
            FROM
                sessions s
            LEFT JOIN sessiontime t ON t.sessiontime_id = s.sessiontime_id
            LEFT JOIN cte_cinema c ON c.cinemaid = t.cinemaid
            LEFT JOIN movies m ON m.movieid = s.movieid
            LEFT JOIN dates d ON d.date = s.session_date
            LEFT JOIN cte_seats cs on cs.sessionid = s.sessionid
            WHERE
                -- timestamp(s.session_date, t.sessiontime) > current_timestamp
                s.session_date <= (
                    SELECT MAX(date)
                    FROM dates
                )
                AND m.movieid = %s
            ORDER BY is_current desc, 
                s.session_date, s.sessionid, m.movieid, m.title, c.name, d.weekday_name, t.sessiontime;
        """
            cursor.execute(sql, (current_timestamp, movieid))

        else:
            # Only schedules that are active from current time, the shchedules that are in the past will not be shown.
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = """
                with cte_seats as (
                    select s.sessionid, count(bs.seatid) as booked_seats
                    from bookings b
                    left join sessions s on s.sessionid = b.sessionid
                    left join booking_seats bs on bs.bookingid = b.bookingid
                    where s.session_date >= %s
                    group by s.sessionid
                )
                ,cte_cinema as (
                    select c.cinemaid, c.name, count(s.seatid) as cinema_seats
                    from cinemas c
                    left join seats s on s.cinemaid = c.cinemaid
                    group by c.cinemaid, c.name
                )
                SELECT
                    m.title,
                    m.movieid,
                    DATE_FORMAT(s.session_date, '%%d/%%m/%%Y') AS sd,
                    s.sessionid,
                    c.name,
                    d.weekday_name,
                    TIME_FORMAT(t.sessiontime, '%%h:%%i %%p') AS sessiontime_12hrs
                    ,case when cs.booked_seats is null then 0 else cs.booked_seats end as booked_seats
                    ,c.cinema_seats
                    ,case when cs.booked_seats is null then c.cinema_seats else c.cinema_seats - cs.booked_seats end as available_seats
                    ,1 as is_current 
                FROM
                    sessions s
                LEFT JOIN sessiontime t ON t.sessiontime_id = s.sessiontime_id
                LEFT JOIN cte_cinema c ON c.cinemaid = t.cinemaid
                LEFT JOIN movies m ON m.movieid = s.movieid
                LEFT JOIN dates d ON d.date = s.session_date
                LEFT JOIN cte_seats cs on cs.sessionid = s.sessionid
                WHERE
                    timestamp(s.session_date, t.sessiontime) > %s
                    AND s.session_date <= (
                        SELECT MAX(date)
                        FROM dates
                    )
                ORDER BY
                    s.session_date, s.sessionid, m.movieid, m.title, c.name, d.weekday_name, t.sessiontime;
            """
            cursor.execute(sql, (current_date, current_timestamp,))
        display_schedules = cursor.fetchall() # list for displaying in movie schedule page
        return render_template('movie_schedule_home.html',last_date=last_date,movies=movies,display_schedules=display_schedules)
    else:
        return redirect(url_for('staff_login.stafflogin'))


@movie_schedule.route('/edit/schedule', methods=['GET', 'POST'])
def edit_schedule():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'GET':
            # these information is from the edit button on that row and only edit this row.
            movieid = request.args.get("movieid")
     
            unformatted_session_date = request.args.get("session_date")  # it is "dd-mm-yyyy" formate
            date_object = datetime.strptime(unformatted_session_date, '%d/%m/%Y')
            session_date = date_object.strftime('%Y-%m-%d') # convert to "yyyy-mm-dd" formate to update mysql database
       
            sessiontime_str=request.args.get("sessiontime")
         
            #selected_sessiontime format is 00:00, it needs to convert to 00:00:00 format
            sessiontime_obj = datetime.strptime(sessiontime_str, "%I:%M %p")
            sessiontime = sessiontime_obj.strftime("%H:%M:%S")


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM sessions where session_date=%s and movieid=%s;",(session_date,movieid,))
            selected_session=cursor.fetchone()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("""SELECT st.*,c.name FROM sessiontime st
                        JOIN cinemas c ON st.cinemaid=c.cinemaid
                        where sessiontime=%s; """,(sessiontime,))
            selected_sessiontime=cursor.fetchone()
            

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM dates where date=%s;",(session_date,))
            selected_date=cursor.fetchone()
  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM movies where movieid=%s;",(movieid,))
            selected_movie=cursor.fetchone()

            #get the row where the movie title, session_date and cinema_name is unique, then update the session_time.
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("""SELECT st.*,c.name
                            FROM sessiontime st
                            JOIN cinemas c ON st.cinemaid=c.cinemaid
                            WHERE sessiontime_id IN (SELECT sessiontime_id FROM sessiontime)
                            AND sessiontime_id NOT IN (SELECT DISTINCT sessiontime_id FROM sessions WHERE session_date = %s);""", (session_date,))
            available_sessiontimes = cursor.fetchall()
            if available_sessiontimes is not None:
                return render_template('schedule_update.html',datetime = datetime,selected_session=selected_session,selected_sessiontime=selected_sessiontime,selected_movie=selected_movie,selected_date=selected_date,movieid=movieid,session_date=session_date,available_sessiontimes=available_sessiontimes) 
            else:
                available_sessiontimes is None
                return render_template('schedule_update.html',selected_session=selected_session,selected_sessiontime=selected_sessiontime,selected_movie=selected_movie,selected_date=selected_date,movieid=movieid,session_date=session_date,available_sessiontimes=available_sessiontimes) 
            
        else:  #get hidden sessionid to update the session table in database once user update the sessiontime for certain movie as well as certain date.
            sessionid = request.form["sessionid"]
            newsessiontimeid=request.form["newsessiontimeid"]
            print("newsessiontimeid",newsessiontimeid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE sessions SET sessiontime_id=%s WHERE sessionid = %s;",(newsessiontimeid,sessionid,))
            mysql.connection.commit()
            flash("Session ID#{} Updated Successfully!".format(sessionid), "success")
            return redirect(url_for('movie_schedule.manage_schedules'))
    else:
        flash("Plase login as manager or admin to edit movies", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@movie_schedule.route('/manage/schedule_add', methods=['GET', 'POST'])
def schedule_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'POST': 
            newMovieid=request.form['newMovieid'] 
            startDate=request.form['startDate'] 
            endDate=request.form['endDate']  # user select a time period to check available sessions

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM movies where movieid=%s;",(newMovieid,))
            selected_movie =cursor.fetchone() # for passing the movieid to next route to update sessions table
     
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            # only get available sessions after current datetime
            now = datetime.now(timezone('Pacific/Auckland'))
            current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            sql = """
                 with cte_sessions as (
                    select concat(s.sessiontime_id, s.session_date) as used_sessions
                    from sessions s
                    where s.session_date >= %s
                        and s.session_date <= %s
                    )
                select DISTINCT 
                    d.date as session_date
                    , t.sessiontime_id
                    ,time_format(t.sessiontime, '%%h:%%i %%p') as sessiontime
                    ,t.cinemaid
                    ,c.name
                    ,timestamp(d.date,  t.sessiontime) as session_datetime
                from sessiontime t
                left join cinemas c on t.cinemaid = c.cinemaid
                join dates d on
                    d.date >= %s
                    and d.date <= %s
                where concat(sessiontime_id, date) not in 
                    (select distinct used_sessions from cte_sessions)
                and timestamp(d.date,  t.sessiontime) > %s
                order by d.date, sessiontime_id
                """
            cursor.execute(sql, (startDate,endDate, startDate,endDate, current_timestamp))
            available_schedules =list(cursor.fetchall())  # display multiple options for user to select
            return render_template('schedule_add.html',startDate=startDate,endDate=endDate,selected_movie=selected_movie,available_schedules=available_schedules)
        else:
            flash("Unsuccessfully added!", "warning")
            return redirect(url_for('movie_schedule.manage_schedules'))
    else:
        flash("Plase login as manager or admin to add movie schedule", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@movie_schedule.route('/manage/schedule_add_plus', methods=['GET', 'POST'])
def schedule_add_plus():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'POST': 
            movieid=int(request.form['movieid'])
            date_time_strings = request.form.getlist('newSessions') #values are string and need to convert to date and time format before insert

            date_objects = []
            timeid_objects = []

            for dt_string in date_time_strings:
                date_str, timeid_str = dt_string.split(',') #use comma to sperate the string
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                timeid_object = int(timeid_str)  
                
                date_objects.append(date_object)   
                timeid_objects.append(timeid_object)

            # Now date_objects and time_objects contain the corresponding date and time values
            for i in range(len(date_objects)): 
                date_object = date_objects[i]
                timeid_object = timeid_objects[i]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("INSERT INTO sessions (session_date, sessiontime_id, movieid) VALUES (%s, %s, %s);",(date_object, timeid_object, movieid,))
                mysql.connection.commit() # insert every row date in list into database 
        flash("Successfully added new movie schedule(s)!", "success")
        return redirect(url_for('movie_schedule.manage_schedules'))
    else:
        flash("Plase login as manager or admin to add movie schedule", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@movie_schedule.route('/delete/schedule', methods=['GET', 'POST'])
def delete_schedule(): 
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'GET':
            # these information is from the delete button on that row and only delete this row.
            movieid = request.args.get("movieid")
            session_date_string = request.args.get("session_date") # it is "dd-mm-yyyy" formate string
            date_object = datetime.strptime(session_date_string, '%d/%m/%Y')
            session_date = date_object.strftime('%Y-%m-%d') # convert to "yyyy-mm-dd" formate to update mysql database

            #get this values from routes and will be deleted
            sessiontime_str=request.args.get("sessiontime")
         
            #selected_sessiontime format is 00:00, it needs to convert to 00:00:00 format
            sessiontime_obj = datetime.strptime(sessiontime_str, "%I:%M %p")
            sessiontime = sessiontime_obj.strftime("%H:%M:%S")
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM sessions where session_date=%s and movieid=%s;",(session_date,movieid,))
            selected_session=cursor.fetchone()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("""SELECT st.*,c.name FROM sessiontime st
                            JOIN cinemas c ON st.cinemaid=c.cinemaid
                            where sessiontime=%s; """,(sessiontime,))
            selected_sessiontime=cursor.fetchone()
            print("selected_sessiontime",selected_sessiontime)


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM dates where date=%s;",(session_date,))
            selected_date=cursor.fetchone()
  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM movies where movieid=%s;",(movieid,))
            selected_movie=cursor.fetchone()

            #get the row where the movie title, session_date and cinema_name is unique, then update the session_time.
            return render_template('schedule_delete.html',selected_session=selected_session,selected_sessiontime=selected_sessiontime,selected_movie=selected_movie,selected_date=selected_date,movieid=movieid,session_date=session_date) 
        
        else:  #get hidden sessionid to update the session table in database once user update the sessiontime for certain movie as well as certain date.
            sessionid = request.form['sessionid']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM sessions WHERE sessionid = %s;",(sessionid,))
            mysql.connection.commit()
            flash("Session ID#{} Deleted Successfully!".format(sessionid), "success")
            return redirect(url_for('movie_schedule.manage_schedules'))
    else:
        flash("Plase login as manager or admin to delete movie schedule", "warning")
        return redirect(url_for('staff_login.stafflogin'))
  
 