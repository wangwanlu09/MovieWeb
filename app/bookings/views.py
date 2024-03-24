
from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session,request,jsonify,abort,flash
import datetime,json
from datetime import date, datetime, timedelta, time
import MySQLdb.cursors,re
from pytz import timezone

booking = Blueprint('booking', __name__)


@booking.route('/select_session/tickets',methods=['GET'])     
def select_tickets():
    # if 'loggedin' in session and session['role'] == 'customer':
    movieid = request.args.get('movieid')  # get these two id to get ready for dispaly that user chose
    sessionid = request.args.get('sessionid')

    now = datetime.now(timezone('Pacific/Auckland'))
    localdate = now.strftime("%Y-%m-%d")
    

    #Get the promotionid for payment part
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute("""SELECT 
                    c.*,
                    s.*,
                    TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours
                    ,st.sessiontime
                    ,timestamp(s.session_date, st.sessiontime) as session_datetime
                FROM
                    cinemas c
                JOIN
                    sessiontime st ON c.cinemaid = st.cinemaid
                JOIN
                    sessions s ON st.sessiontime_id = s.sessiontime_id
                WHERE s.sessionid= %s;""",(sessionid,))
    selected_session=cursor.fetchone() # get selected session_date to get weekday name
    session_date=selected_session['session_date']  
    session_datetime = selected_session['session_datetime'].strftime("%Y-%m-%d %H:%M:%S")

    # Tuesday daytime 7am - 7pm
    startTime = timedelta(hours=7, minutes=0, seconds=0)
    endTime = timedelta(hours=19, minutes=0, seconds=0)

    # check session date and time 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    # check if it is Tuesday
    if session_date.weekday() == 1 and selected_session['sessiontime'] >= startTime and selected_session['sessiontime'] <= endTime:
        # check if there is promotion set up
        cursor.execute("""SELECT t.* FROM tickets t where is_fixed = 1;""")
        tickets=cursor.fetchall()
        # if promotion day is not set up or session is out of daytime
        cursor.execute("select * from promotions where promotion_type_id = 1 and is_active = 1")
        promotion = cursor.fetchone()
        if tickets and promotion:
            is_tuesday = 1
        else:
            is_tuesday = 0
            cursor.execute("""SELECT t.* FROM tickets t where is_fixed = 0;""")
            tickets=cursor.fetchall()
 
    else:
        cursor.execute("""SELECT t.* FROM tickets t where is_fixed = 0;""")
        tickets=cursor.fetchall()
        # now = datetime.now(timezone('Pacific/Auckland'))
        # today = now.strftime("%Y-%m-%d")
        # date7 = now + timedelta(days=6)
        sql = """
            select * from promotions 
            where promotion_type_id = 2 
            and is_active = 1 
            and effective_date <= %s and expiration_date >= %s
            """
        cursor.execute(sql, (session_datetime, session_datetime))
        promotion = cursor.fetchone()
        is_tuesday = 0
    
    #remaining seats for new bookings
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute("""SELECT
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
                );""",(sessionid,))
    remaining_seats=cursor.fetchone()
   


    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute("SELECT * FROM dates WHERE date=%s;",(session_date,))
    selected_date=cursor.fetchone() # for displaying weekday and date

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    cursor.execute( """
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
            where m.movieid= %s;""",(movieid,))
    selected_movie=cursor.fetchone() #all the info of the selected movie for displaying
    return render_template('booking_tickets.html', selected_session=selected_session,selected_movie=selected_movie,selected_date=selected_date,tickets=tickets,\
                            is_tuesday=is_tuesday, promotion=promotion,remaining_seats=remaining_seats)

 
@booking.route('/select_seats', methods=['POST'])
def select_seats():

    # get all this values from hidden form
    total_price_numeric = request.form.get('hidden_totalPrice')
    total_count = request.form.get('hidden_totalCount')
    movieid = request.form.get('hidden_movieid')
    cinemaid = request.form.get('hidden_cinemaid')
    sessionid =request.form.get('hidden_sessionid')
    # promotionid=request.form.get('hidden_promotionid')
    ticket_quantities_dict=request.form.get('hidden_ticketQuantities')

    if not total_price_numeric: # Handle the case when total_price_numeric is None (e.g., on page refresh)
        return redirect(url_for('request.referrer')) # redirect the user to the previous page page if it is none
    total_price = float(total_price_numeric)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM cinemas WHERE cinemaid=%s;",(cinemaid,))
    selected_cinema=cursor.fetchone() # for displaying weekday and date
    # Close the cursor after fetching the data
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM seats WHERE cinemaid=%s;",(cinemaid,))
    seats=cursor.fetchone() # for displaying weekday and date
    # Close the cursor after fetching the data
    cursor.close()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
                    with cte as (
                    select c.cinemaid, c.name, count(s.seatid) as no_of_seats
                    from cinemas c
                    left join seats s on s.cinemaid = c.cinemaid
                    group by c.cinemaid, c.name
                    )
                    SELECT
                    s.sessionid,
                    s.session_date,
                    st.sessiontime_id,
                    st.sessiontime,
                    c.cinemaid,
                    c.name AS cinema_name,
                    c.no_of_seats AS cinema_seats,
                    se.seatid,
                    se.seat_number
                FROM
                    sessions AS s
                INNER JOIN sessiontime AS st ON s.sessiontime_id = st.sessiontime_id
                INNER JOIN cte AS c ON st.cinemaid = c.cinemaid
                INNER JOIN seats AS se ON c.cinemaid = se.cinemaid
                where s.sessionid=%s
                ORDER BY
                    s.sessionid, st.sessiontime_id, se.seat_number ;""",(sessionid,))
    available_seesions=cursor.fetchall() # for displaying available seats
    available_seats_info = [(s['seatid'], s['seat_number']) for s in available_seesions]
    cursor.close()

    # this query to get occupied seat from booking and booking_seats tables, occupied seats will be shown until users have new bookings.
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT
                        b.*,
                        bs.bsid,
                        bs.seatid
                    FROM
                        bookings AS b
                    INNER JOIN
                        booking_seats AS bs ON b.bookingid = bs.bookingid WHERE b.sessionid=%s ;""",(sessionid,))
    exsiting_bookings=cursor.fetchall() # for displaying the booking info in this session, and get the seatid for seat map
    occupied_seats = [(b['sessionid'], b['seatid']) for b in exsiting_bookings]
    cursor.close()
    return render_template('select_seats.html',available_seats_info=available_seats_info,occupied_seats=occupied_seats,ticket_quantities_dict=ticket_quantities_dict, total_price=total_price,total_count=total_count,movieid=movieid,cinemaid=cinemaid, selected_cinema=selected_cinema,seats=seats,sessionid=sessionid,total_price_numeric=total_price_numeric)



@booking.route('/view_payment', methods=['GET'])     
def view_payment():
    if 'loggedin' in session and session['role'] == 'customer':
        seatsValue = request.args.getlist('seatsValue',type=int)
        total_price_numeric = request.args.get('total_price_numeric')
        total_count = request.args.get('total_count')
        movieid = request.args.get('movieid')
        cinemaid = request.args.get('cinemaid')
        sessionid = request.args.get('sessionid')
        
        print("Received seatsValue:", seatsValue)
        print("Received total_price_numeric:", total_price_numeric)
        print("Received total_count:", total_count)
        print("Received movieid:", movieid)
        print("Received cinemaid:", cinemaid)
        print("Received sessionid:", sessionid)

        # return f"Received seatValue again: {seatsValue}, total_price_numeric: {total_price_numeric}, total_count: {total_count}, movieid: {movieid}, cinemaid: {cinemaid}, sessionid: {sessionid}"
        return render_template('test2.html', data=seatsValue)
    else:
        flash("Please log in as customer", "warning")
        return redirect(url_for('customer_login.customerlogin'))

@booking.route('/add_seats',methods=['POST'])
def add_seats():  
    data = request.get_json()
    session['booking_seats'] = data['seatsValue']
    session['booking_sessionid'] = data['sessionid']
    session['booking_tickets'] = data['ticket_quantities_dict']
    session['booking_amount'] = data['total_price_numeric']
    # check if customer is logged in
    if 'loggedin' in session and session['role'] == 'customer':
        return redirect(url_for('payments.payment_booking'))
    else:
        session['booking_url'] = True
        flash("Please log in to continue", "warning")
        return redirect(url_for('customer_login.customerlogin'))

@booking.route("/booking_information")
def booking_history():
    if 'loggedin' in session and session['role'] == 'customer':
        now = datetime.now(timezone('Pacific/Auckland'))
        current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            with cte_seats as (
                select bookingid, GROUP_CONCAT(s.seat_number SEPARATOR ', ') as seats
                from booking_seats bs
                left join seats s on s.seatid = bs.seatid
                group by bookingid
            )
            , cte_ticket as (
                select bookingid,  GROUP_CONCAT(concat(t.ticket_type, ' X ', bk.no_of_tickets ) SEPARATOR ', ') as tickets
                from booking_transactions bk 
                left join tickets t on t.ticketid = bk.ticketid
                group by bookingid
            )
            SELECT
                m.title AS movie_title,
                b.bookingid,
                b.total_amount,
                b.payment_amount,
                c.name,
                ses.session_date,
                TIME_FORMAT(ti.sessiontime, '%%h:%%i %%p') AS sessiontime
                ,case when timestamp(ses.session_date,  ti.sessiontime) > %s then 1 else 0 end as is_available
                ,ct.tickets
                ,bs.seats
                ,b.booking_date
            FROM
                bookings b
                JOIN sessions ses ON b.sessionid = ses.sessionid
                JOIN sessiontime ti ON ses.sessiontime_id = ti.sessiontime_id
                JOIN movies m ON ses.movieid = m.movieid
                JOIN cte_ticket ct on ct.bookingid = b.bookingid
                JOIN cte_seats bs ON b.bookingid = bs.bookingid
                JOIN cinemas c ON ti.cinemaid = c.cinemaid
                left join customers cu on cu.customerid = b.customerid
            WHERE
                cu.accountid =  %s
            ORDER BY b.bookingid DESC
        """

        cursor.execute(sql, (current_timestamp, session['accountid']))
        bookings = cursor.fetchall()

        
        return render_template("booking_detail.html", bookings=bookings, datetime=datetime, now=now) 
    else:
        flash("Please log in as customer", "warning")
        return redirect(url_for('customer_login.customerlogin'))

@booking.route('/mybooking/ticketpreview')
def ticket_preview():
    if 'loggedin' in session and session['role'] == 'customer':
        bookingid = request.args.get('bookingid')
        sql_tickets = """
            select s.seat_number  
            from booking_seats bs
            left join seats s on s.seatid = bs.seatid
            where bookingid = %s
            """
        sql_session = """
            select b.bookingid
                ,m.title
                ,c.name
                ,s.session_date
                ,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS sessiontime
            from bookings b
            left join sessions s on s.sessionid = b.sessionid
            left join sessiontime st on st.sessiontime_id = s.sessiontime_id
            left join cinemas c on c.cinemaid = st.cinemaid
            left join movies m on m.movieid = s.movieid
            where b.bookingid = %s
            """
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_tickets, (bookingid, ))
        seats = cursor.fetchall()
        cursor.execute(sql_session, (bookingid, ))
        sessioninfo = cursor.fetchone()
        return render_template('ticket_print.html', seats=seats, sessioninfo=sessioninfo)
    else:
        flash("Please log in as customer", "warning")
        return redirect(url_for('customer_login.customerlogin'))