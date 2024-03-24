
from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session,request,jsonify,abort,flash
import datetime,json
from datetime import date, datetime, timedelta
import MySQLdb.cursors,re
from pytz import timezone

checkIn = Blueprint('checkIn', __name__)


@checkIn.route('/session_checkin',methods=['GET'])     
def session_checkin():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        if request.method == 'GET':
             #The list display the infomation for all session which need to check in. 
            now = datetime.now(timezone('Pacific/Auckland'))
            localdate = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M:%S")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("""SELECT s.sessionid,s.sessiontime_id, DATE_FORMAT(s.session_date,'%%d/%%m/%%Y') AS sd,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS sessiontime_12hrs,m.title,c.name FROM sessions s 
                            LEFT JOIN movies m ON s.movieid=m.movieid
                            LEFT JOIN sessiontime st ON s.sessiontime_id=st.sessiontime_id
                            LEFT JOIN cinemas c ON st.cinemaid=c.cinemaid
                            WHERE s.session_date = %s and st.sessiontime > %s order by s.sessionid;""",(localdate,current_time,))
            today_session_list=cursor.fetchall()
            return render_template('check_session_tickets.html',today_session_list=today_session_list)

    else:
        flash("Plase login as a staff, manager or admin to update ticket check status", "warning")
        return redirect(url_for('staff_login.stafflogin'))



@checkIn.route('/check_in_ticket',methods=['GET','POST'])     
def check_in_ticket():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        if request.method == 'GET':
            #Get value from url
            sessionid=request.args.get('sessionid')
           
            #The list display the infomation in customer's ticket
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            sql = """
                with cte_sessionseats as (
                SELECT s.sessionid,m.title, m.movieid, c.name,s.session_date,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS sessiontime_12hrs
                ,se.seatid, se.seat_number
                FROM sessions s 
                LEFT JOIN sessiontime st ON st.sessiontime_id=s.sessiontime_id
                LEFT JOIN cinemas c ON st.cinemaid=c.cinemaid
                LEFT JOIN seats se ON se.cinemaid = c.cinemaid
                LEFT JOIN movies m ON s.movieid=m.movieid
                WHERE s.sessionid= %s 
                )
                ,cte_bookingseats as (
                SELECT b.sessionid, bs.seatid, bs.is_checkin,bs.bsid
                FROM bookings b 
                LEFT JOIN booking_seats bs ON b.bookingid = bs.bookingid
                LEFT JOIN seats s1 on s1.seatid = bs.seatid
                WHERE b.sessionid= %s 
                )
                select s.*, b.bsid
                ,case when b.is_checkin is not null then b.is_checkin else 0 end as is_checkin
                ,case when b.seatid is not null then 1 else 0 end as is_booked
                from cte_sessionseats s
                left join cte_bookingseats b on b.sessionid = s.sessionid 
                    and b.seatid = s.seatid
                order by b.seatid is null, s.seatid
                """
            cursor.execute(sql, (sessionid, sessionid))
            ticket_check_list=cursor.fetchall()
            return render_template('check_tickets.html',ticket_check_list=ticket_check_list)
        else:
             # Access the value of the selected radio from the hidden input field
            selected_radio_value = request.form.get('selectedRadioValue')
            bsid = request.form.get('bsidValue')
            sessionid=request.form.get('sessionid')

            #update the database when user change status
            if selected_radio_value == 'Not_Checked':  
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE booking_seats SET is_checkin = '0' WHERE bsid = %s;",(bsid,))
                mysql.connection.commit()
                status = "Not Checked In"
            elif selected_radio_value == 'Checked':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE booking_seats SET is_checkin = '1' WHERE bsid = %s;",(bsid,))
                mysql.connection.commit()
                status = "Checked In"
            #Ticket Check ID is also bsid 
            flash("Update Ticket Check ID #{} is now {} ".format(bsid, status), 'success')  
            return redirect(url_for('checkIn.check_in_ticket',sessionid=sessionid))    
    else:
        flash("Plase login as a staff, manager or admin to update ticket check status", "warning")
        return redirect(url_for('staff_login.stafflogin'))