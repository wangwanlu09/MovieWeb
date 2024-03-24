from app import mysql
import datetime
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from pytz import timezone


detailed = Blueprint('detailed', __name__)


@detailed.route('/details/movie')
def Movie_details():
    movieid = request.args.get('movieid')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql1 = """
        with cte_star AS (
            select s.movieid 
                ,GROUP_CONCAT(a.actor_name SEPARATOR ', ') as starring
            from starring s
            left join actors a on a.actorid = s.actorid
            where s.latest_version = 1 and s.movieid = %s
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
            where m.movieid = %s
            and m.movieid in (
                select distinct movieid
                from sessions 
                where session_date between %s and %s
            );
        """ 
    today = datetime.now(timezone('Pacific/Auckland'))
    date7 = today + timedelta(days=6)
    parameters = (movieid, movieid, today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'))
    cursor.execute(sql1, parameters)
    movie_detail_info = cursor.fetchone()

    now = datetime.now()
    current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    sql5 = """
        SELECT
            s.session_date,
            st.sessiontime
        FROM
            sessions s
            JOIN sessiontime st ON s.sessiontime_id = st.sessiontime_id
        WHERE
            s.movieid = %s
            AND timestamp(s.session_date,  st.sessiontime) > %s;

    """

    cursor.execute(sql5, (movieid, current_timestamp))
    sessions = cursor.fetchall()

    current_date = today
    format_time = current_date.strftime('%d/%m')
    date_array = [current_date + timedelta(days=i) for i in range(7)]
    formatted_dates = [date.strftime('%Y/%d/%m %a').upper() for date in date_array]
    return render_template('movie_detail.html', movie=movie_detail_info,  sessions=sessions, formatted_dates=formatted_dates, format_time=format_time)


@detailed.route('/load_data/')
def load_data():
    # get date information
    month_str = request.args.get("month")
    date_object = datetime.strptime(month_str, '%Y/%d/%m')
    month = date_object.strftime('%Y-%m-%d') 
    # sessionid=request.args.get("sessionid")
    # print("sessionid",sessionid)
    
    movieid = request.args.get("movieid")

    now = datetime.now(timezone('Pacific/Auckland'))
    current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

   
    # session are the valid session on the session_date 
    # it needs to sort out the session where is fully booked  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql2 = """
        SELECT * FROM (
        SELECT s.sessionid, s.session_date, s.sessiontime_id, s.movieid, TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours, st.maximum_time, st.cinemaid
        FROM sessions s
        LEFT JOIN sessiontime st ON s.sessiontime_id = st.sessiontime_id
        WHERE movieid = %s
        AND timestamp(s.session_date, st.sessiontime) > %s
        ORDER BY s.session_date, st.sessiontime
        ) AS t1
        WHERE (t1.sessionid, t1.session_date, t1.sessiontime_id, t1.movieid, t1.session12hours, t1.maximum_time, t1.cinemaid)
        IN (
        SELECT s2.sessionid, s2.session_date, s2.sessiontime_id, s2.movieid, TIME_FORMAT(st2.sessiontime, '%%h:%%i %%p') AS session12hours, st2.maximum_time, st2.cinemaid
        FROM sessions s2
        LEFT JOIN sessiontime st2 ON s2.sessiontime_id = st2.sessiontime_id
        WHERE movieid = %s
        AND timestamp(s2.session_date, st2.sessiontime) > %s
        AND s2.session_date =  %s
        ORDER BY s2.session_date, st2.sessiontime);
        """
    
    cursor.execute(sql2,(movieid,current_timestamp,movieid,current_timestamp,month))
    sessions = cursor.fetchall()
    print("session are ",sessions)
 

    # get all the sessionid on the selected date and movieid, normally there will be 1-4 sessions.
    sessionids = [ id['sessionid']  for id in sessions]
 
    remaining_seats_list = []

    for sessionid in sessionids:
        sql6 = """
            SELECT
                s.sessionid,
                count(se.seatid) as no_of_seats
            FROM
                sessions s
            INNER JOIN
                sessiontime st ON st.sessiontime_id = s.sessiontime_id
            INNER JOIN 
                seats se ON st.cinemaid= se.cinemaid
            WHERE
                s.sessionid = %s
                AND NOT EXISTS (
                    SELECT 1
                    FROM
                        booking_seats bs
                    INNER JOIN
                        bookings b ON bs.bookingid = b.bookingid
                    WHERE
                        b.sessionid = s.sessionid
                        AND bs.seatid = se.seatid
                );
            """
        cursor.execute(sql6, (sessionid,))
        remaining_seats = cursor.fetchone()
        remaining_seats_list.append(remaining_seats)
    print("remaining_seats_list",remaining_seats_list)

    return render_template('content1.html', movieid=movieid,sessions=sessions, month=month,remaining_seats_list=remaining_seats_list)


@detailed.route('/booking/sessiontime_id')
def booking():
    movieid = request.args.get('movieid')
    sessiontime_id = request.args.get('sessiontime_id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        with cte_star AS (
            select s.movieid 
                ,GROUP_CONCAT(a.actor_name SEPARATOR ', ') as starring
            from starring s
            left join actors a on a.actorid = s.actorid
            where s.latest_version = 1 and s.movieid = %s
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
            where m.movieid = %s
            and m.movieid in (
                select distinct movieid
                from sessions 
                where session_date between %s and %s
            );
        """
    today = datetime.now(timezone('Pacific/Auckland'))
    date7 = today + timedelta(days=6)
    parameters = (movieid, movieid, today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters)
    movie_detail_info = cursor.fetchone()
    
    return render_template('booking.html', movie=movie_detail_info, sessiontime_id=sessiontime_id)
