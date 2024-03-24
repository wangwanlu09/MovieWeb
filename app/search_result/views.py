from app import mysql
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from pytz import timezone

search_result = Blueprint('search_result', __name__)
@search_result.route('/search_result')
def searchresult():
    search = request.args.get('Search')
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
        ,RecentSessions AS (
            SELECT 
                movieid,
                MIN(session_date) AS min_session_date,
                MAX(session_date) AS max_session_date
            FROM 
                sessions
            WHERE 
                session_date BETWEEN %s AND %s
            GROUP BY 
                movieid
        )
        ,final as (
        select 
            m.*, m.runtime_hour * 60 + runtime_minute as runtime
            ,g.genre_name
            ,r.rating_code, r.color 
            ,cs.starring 
            ,r.min_session_date
        from movies m
        left join RecentSessions r on r.movieid = m.movieid
        left join genre g on g.genreid = m.genreid
        left join ratings r on r.ratingid = m.ratingid
        left join cte_star as cs on cs.movieid = m.movieid
        where m.movieid in (
            select distinct movieid
            from sessions 
            where session_date between %s and %s
        )
        or m.start_date between %s and %s
        )
        select * from final
        where title like %s
        or descriptions like %s
        or starring like %s
    """

    today = date.today()
    date7 = today + timedelta(days=6)
    today7 = today + timedelta(days=7)
    today30 = today + timedelta(days=30)
    parameters = (today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), date7.strftime('%Y-%m-%d'), today7.strftime('%Y-%m-%d'), today30.strftime('%Y-%m-%d'))
    cursor.execute(sql, parameters + (f"%{search}%", f"%{search}%", f"%{search}%",))
    search_results = cursor.fetchall()
    return render_template('search_results.html', search_results=search_results)