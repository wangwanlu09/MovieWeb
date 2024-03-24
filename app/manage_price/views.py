from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session,request,jsonify,abort,flash
import datetime,json
from datetime import date, datetime, timedelta
import MySQLdb.cursors
from pytz import timezone

ticket_price = Blueprint('ticket_price', __name__)

@ticket_price.route('/manage/ticket_prices',methods=['GET'])     
def manage_ticket_prices():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        now = datetime.now(timezone('Pacific/Auckland'))
        localdate = now.strftime("%Y-%m-%d %H:%M:%S")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""WITH cte AS (
                            SELECT tp.tpid, tp.is_percentage, tp.promotionid, tp.ticketid  
                            ,case when is_percentage = 0 then tp.discounted_price else t.price - (t.price * convert(tp.discount_percentage, decimal(5,2))/100) end as discounted_price
                            ,case when is_percentage = 1 then tp.discount_percentage else (t.price - convert(tp.discounted_price, decimal(5,2)))/t.price * 100 end as discount_percentage
                            FROM ticket_promotion tp
                            LEFT JOIN promotions p ON p.promotionid = tp.promotionid
                            LEFT JOIN tickets t ON t.ticketid = tp.ticketid
                            WHERE latest_version = 1
                            AND expiration_date > %s
                            AND p.is_active = 1
                        )
                        SELECT t.*, c.tpid, c.promotionid, c.discounted_price, c.discount_percentage 
                        FROM tickets t
                        LEFT JOIN cte c ON t.ticketid = c.ticketid;""", (localdate,))
        tickets=cursor.fetchall()
        ticket_ids = [entry['ticketid'] for entry in tickets if 'ticketid' in entry]
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
        cursor.execute("SELECT * FROM tickets;")
        available_ticket_types=cursor.fetchall()

        return render_template('manage_price.html',tickets=tickets,ticket_ids=ticket_ids,available_ticket_types=available_ticket_types)


@ticket_price.route('/ticket/price/add',methods=['GET','POST'])     
def add_ticket_price():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'POST':
 
            ticket_type=request.form['ticket_type'].strip()
            Price=request.form['Price']
 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("INSERT INTO tickets (ticket_type, price) VALUES (%s, %s);",(ticket_type,Price,))
            mysql.connection.commit()
            flash("New ticket price added successfully!", "success")
            return redirect(url_for('ticket_price.manage_ticket_prices'))
        else:
            flash("Added Unsuccessfully!", "warning")
            return redirect(url_for('ticket_price.manage_ticket_prices'))
    else:
        flash("Plase login as manager or admin to update ticket price", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@ticket_price.route('/ticket/price/edit',methods=['GET','POST'])     
def edit_ticket_prices():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):

        ticketid=request.args.get('ticketid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
        cursor.execute("SELECT * FROM tickets WHERE ticketid=%s;",(ticketid,))
        tickets=cursor.fetchone()
        return render_template('manage_price_update.html',ticketid=ticketid,tickets=tickets)

    else:
        flash("Plase login as manager or admin to update ticket price", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@ticket_price.route('/ticket/price/update',methods=['POST']) 
def ticket_price_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        ticketid=request.form['ticket_id']
        new_price=request.form['new_price']
        # tueTicket = request.form['tueTicket']
        ticket_type = request.form['ticket_type']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
        cursor.execute("UPDATE tickets SET ticket_type=%s, price=%s WHERE ticketid = %s;",(ticket_type, new_price,ticketid))
        mysql.connection.commit()

        flash("ID #{} Price updated successfully!".format(ticketid), "success")
        return redirect(url_for('ticket_price.manage_ticket_prices'))

@ticket_price.route('/delete_ticke_prices',methods=['GET','POST'])     
def delete_ticke_prices():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'GET':
            ticketid=request.args.get('ticketid')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
            cursor.execute("SELECT * FROM tickets WHERE ticketid=%s;",(ticketid,))
            ticket=cursor.fetchone()
            return render_template('manage_price_delete.html',ticketid=ticketid,ticket=ticket)
        else:
            ticketid = request.form['ticketid']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM tickets WHERE ticketid = %s;",(ticketid,))
            mysql.connection.commit()
            flash("ID #{} ticket price deleted successfully!".format(ticketid), "success") 
            return redirect(url_for('ticket_price.manage_ticket_prices'))
    else:
        flash("Plase login as manager or admin to delete ticket price", "warning")
        return redirect(url_for('staff_login.stafflogin'))
