from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
import json
from pytz import timezone

payments = Blueprint('payments', __name__)

@payments.route('/payment/booking')
def payment_booking():
    if 'loggedin' in session and session['role'] == 'customer':
        booking_seats = session['booking_seats']
        booking_tickets = json.loads(session['booking_tickets'])
        # movie info
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql_session_movie = """
            select 
                m.*, m.runtime_hour * 60 + runtime_minute as runtime
                ,g.genre_name
                ,r.rating_code, r.color
                ,s.sessionid
                ,s.session_date
                ,st.sessiontime
                ,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours
                ,timestamp(s.session_date, st.sessiontime) as session_datetime
                ,c.name
            from sessions s
            left join sessiontime st on st.sessiontime_id = s.sessiontime_id
            left join cinemas c on c.cinemaid = st.cinemaid
            left join movies m on s.movieid = m.movieid
            left join genre g on g.genreid = m.genreid
            left join ratings r on r.ratingid = m.ratingid
            where s.sessionid = %s
            """
        cursor.execute(sql_session_movie, (session['booking_sessionid'],))
        movie = cursor.fetchone()

        # Tuesday cannot apply promotion code
        # Tuesday daytime 7am - 7pm
        startTime = timedelta(hours=7, minutes=0, seconds=0)
        endTime = timedelta(hours=19, minutes=0, seconds=0)
        session_datetime = movie['session_datetime'] 

        if session_datetime.weekday() == 1 and movie['sessiontime'] >= startTime and movie['sessiontime'] <= endTime:
            # check if there is promotion set up
            cursor.execute("""SELECT t.* FROM tickets t where is_fixed = 1;""")
            check_tickets=cursor.fetchall()
            # if promotion day is not set up or session is out of daytime
            cursor.execute("select * from promotions where promotion_type_id = 1")
            check_promotion = cursor.fetchone()
            if check_tickets and check_promotion:
                is_tuesday = 1
            else:
                is_tuesday = 0
        else:
            is_tuesday = 0

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from tickets;")
        price = cursor.fetchall()
        
        tickets =[]
        for key, val in booking_tickets.items():
            if val != 0:
                ticket = {'ticketid': int(key), 'number': val} 
                for p in price:
                    if p['ticketid'] == int(key):
                        ticket['ticketid'] = p['ticketid']
                        ticket['price'] = p['price']
                        ticket['ticket_type'] = p['ticket_type']
                        tickets.append(ticket)

        # seats
        format_strings = ','.join(['%s'] * len(booking_seats))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM seats WHERE seatid IN (%s)" % format_strings,
                tuple(booking_seats))
        seats = cursor.fetchall()
        seat_number = [d['seat_number'] for d in seats]
        seatid = [d['seatid'] for d in seats]

        # valid card expiray date
        today = datetime.now(timezone('Pacific/Auckland'))
        currentmonth = today.strftime('%Y-%m')
        return render_template('payment_booking.html', movie = movie, seatid = seatid, seat_number = seat_number, price = price, tickets = tickets, amount=session['booking_amount'], currentmonth = currentmonth, is_tuesday=is_tuesday)
    else:
        flash("Please log in to continue booking", "warning")
        return redirect(url_for('customer_login.customerlogin'))


@payments.route('/payment/made/booking', methods=['POST'])
def payment_booking_made():   
    if 'loggedin' in session and session['role'] == 'customer':
        ticekts = json.loads(session['booking_tickets'])
        amount = session['booking_amount']
        no_of_tickets = sum(ticekts.values())
        now = datetime.now(timezone('Pacific/Auckland'))
        now_date = now.strftime('%Y-%m-%d')
        now_time = now.strftime('%H:%M:%S')

        if 'from_form' not in request.form.keys():
            gc_deducted = request.form['zero_gcdeducted']
            gcnum = request.form['zero_gcnum']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from giftcards where giftcard_number = %s;", (gcnum, ))
            giftcardid = cursor.fetchone()['giftcardid']
            promodeducted = request.form['zero_promodeducted']
            promocode = request.form['zero_promocode']
            paymentamt = float(amount) - float(gc_deducted) - float(promodeducted)
        elif 'from_form' in request.form.keys() and request.form['py_gcnum'] != "":
            gc_deducted = request.form['py_gcdeducted']
            gcnum = request.form['py_gcnum']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from giftcards where giftcard_number = %s;", (gcnum, ))
            giftcardid = cursor.fetchone()['giftcardid']
            promodeducted = float(request.form['py_promodeducted'])
            promocode = request.form['py_promocode']
            paymentamt = float(amount) - float(gc_deducted) - float(promodeducted)
        else:
            gc_deducted = 0
            giftcardid = None
            promodeducted = float(request.form['py_promodeducted'])
            promocode = request.form['py_promocode']
            paymentamt = float(amount) - float(promodeducted)
        
        if promocode == "":
            promocode = None
        
        # get promotionid
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from promotions where promotion_code = %s", (promocode,))
        promotions = cursor.fetchone()
        if promotions:
            promotionid = promotions['promotionid']
        else:
            promotionid = None
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # 1. update bookings table
        sql_booking = """
                INSERT INTO bookings (no_of_tickets, total_amount, payment_amount, booking_date, booking_time, giftcardid, giftcard_deducted, sessionid, promotion_deducted, promotionid, customerid)
                SELECT
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, c.customerid
                FROM customers c
                JOIN accounts a on a.accountid = c.accountid
                WHERE a.accountid = %s;
            """
        parameters_booking = (no_of_tickets, amount, paymentamt, now_date, now_time, giftcardid, gc_deducted, session['booking_sessionid'], promodeducted, promotionid, session['accountid'])
        cursor.execute(sql_booking, parameters_booking)

        # 2. get the last booking id
        bookingid = cursor.lastrowid

        # 3. update booking_seats table
        for seatid in session['booking_seats']:
            cursor.execute("INSERT INTO booking_seats (bookingid, seatid) VALUES (%s, %s)", (bookingid, int(seatid)))

        # 4. update booking_transaction table
        sql_tickets = """
            with cte as (
                select * from ticket_promotion where promotionid = %s
                )
            select t.*, case when tp.discounted_price is null then t.price else discounted_price end as unitprice
            FROM tickets t
            LEFT JOIN cte tp on tp.ticketid = t.ticketid
            """
        cursor.execute(sql_tickets, (promotionid, ))
        price = cursor.fetchall()
        sql_transactions = """
                INSERT INTO booking_transactions (no_of_tickets, unit_price, bookingid, ticketid, transaction_date, transaction_time)
                VALUES
                (%s, %s, %s, %s, %s, %s)
            """
        for key, val in ticekts.items():
            if val != 0:
                for p in price:
                    if p['ticketid'] == int(key):
                        unit_price = p['unitprice']
                        parameters_trans = (val, unit_price, bookingid, int(key), now_date, now_time)
                        cursor.execute(sql_transactions, parameters_trans)

        # 5. update payment table
        sql_payment = """
                INSERT INTO payment (payment_date, payment_time, amount, payment_type, bookingid, customerid)
                SELECT %s, %s, %s, 'booking', %s, c.customerid
                FROM customers c
                JOIN accounts a on a.accountid = c.accountid
                WHERE a.accountid = %s;
            """
        parameters_payment = (now_date, now_time, paymentamt, bookingid, session['accountid'])
        cursor.execute(sql_payment, parameters_payment)

        # amount should = payment amount after giftcard

        # card number, card holder to payment table

        # commit all the changes above
        mysql.connection.commit()

        # remove booking info in session
        session.pop('booking_seats', None)
        session.pop('booking_sessionid', None)
        session.pop('booking_tickets', None)
        session.pop('booking_amount', None) 

        # redirct to booking history once available
        flash(f"Booking # {bookingid} is done ", "success")
        # return redirect(url_for('booking.booking_history'))
        return redirect('/booking_information')

    else:
        flash("Please log in as a customer", "warning")
        return redirect(url_for('customer_login.customerlogin'))