from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, jsonify
import MySQLdb.cursors,ast
from datetime import datetime, timedelta, time
from pytz import timezone
import string, random

promotions = Blueprint('promotions', __name__)

@promotions.route('/promotions')
def promotion_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now(timezone('Pacific/Auckland'))
    today = now.strftime("%Y-%m-%d")
    date7 = now + timedelta(days=6)
    # weekstart = now - timedelta(days=now.weekday())
    # weekend = weekstart + timedelta(days=6)
    # weekstart = weekstart.strftime("%Y-%m-%d")
    # weekend = weekend.strftime("%Y-%m-%d")
    sql = """
        select *
        from promotions
        where is_active = 1
        and (
           
        cast(effective_date as date) between %s and %s
        or cast(expiration_date as date) between %s and %s
		or promotion_type_id = 1
                
            )
        """
    parameters = (today, date7, today, date7)
    cursor.execute(sql, parameters)
    promotionlist = cursor.fetchall()
    return render_template('promotion_home.html', promotionlist = promotionlist)

@promotions.route('/promotions/detail')
def promotion_home_detail():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    promotionid = request.args.get('promotionid')
    now = datetime.now(timezone('Pacific/Auckland'))
    if promotionid == '' or promotionid == None:
        localdate = now.strftime("%Y-%m-%d")
        cursor.execute('select * from promotions where cast(effective_date as date) <= %s and cast(expiration_date as date) >= %s and is_active = 1', (localdate, localdate))
        promotion = cursor.fetchone()
    else:
        cursor.execute("select * from promotions where promotionid = %s", (promotionid, ))
        promotion = cursor.fetchone()
        if promotion['promotion_type_id'] in [1, 2]: # price discount by promotion code
            sql = """
                select t.*
                    ,case when is_percentage = 0 then tp.discounted_price else t.price - (t.price * convert(tp.discount_percentage, decimal(5,2))/100) end as discounted_price
                    ,case when is_percentage = 1 then tp.discount_percentage else (t.price - convert(tp.discounted_price, decimal(5,2)))/t.price * 100 end as discount_percentage
                    -- ,t.price - tp.discounted_price as savenum
                from ticket_promotion tp 
                left join tickets t on tp.ticketid = t.ticketid 
                where tp.latest_version = 1
                and tp.promotionid = %s
                and t.is_fixed = 0
                """
            cursor.execute(sql, (promotionid, ))
            tickets = cursor.fetchall()

            if promotion['promotion_type_id'] == 1:
                if now.weekday() < 1:
                    nextTueDate = now + timedelta(days=1)
                else:
                    nextTueDate = now + timedelta(days=(8 - now.weekday()))
                # Tuesday Daytime
                fromDT = nextTueDate.strftime("%Y-%m-%d") + " " + "07:00:00"
                toDT = nextTueDate.strftime("%Y-%m-%d") + " " + "19:00:00"
            else:
                fromDT = promotion['effective_date']
                toDT = promotion['expiration_date']

            sql_movies = """
                    select 
                        m.*, m.runtime_hour * 60 + runtime_minute as runtime
                        ,g.genre_name, r.rating_code, r.color  
                    from movies m
                    left join genre g on g.genreid = m.genreid
                    left join ratings r on r.ratingid = m.ratingid
                    where m.movieid in (
                        select distinct s.movieid
                        from sessions s
                        left join sessiontime st on st.sessiontime_id = s.sessiontime_id 
                        where timestamp(s.session_date, st.sessiontime) between %s and %s
                    );
                """
            cursor.execute(sql_movies, (fromDT, toDT))
            movies = cursor.fetchall()

            sql_sessions = """
                select s.*
                    ,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours
                from sessions s
                left join sessiontime st on st.sessiontime_id = s.sessiontime_id 
                where timestamp(s.session_date, st.sessiontime) between %s and %s
                ORDER BY s.session_date, st.sessiontime
                """
            cursor.execute(sql_sessions, (fromDT, toDT))
            tueSessions = cursor.fetchall()
            return render_template('promotion_home_detail.html', promotion = promotion, tickets = tickets, movies=movies,  tueSessions=tueSessions)
        
    return render_template('promotion_home_detail.html', promotion = promotion, tickets = None)



@promotions.route('/promotions/manage')
def promotion_view():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select p.*, t.promotion_type, t.descriptions as type_desc from promotions p left join promotion_types t on p.promotion_type_id = t.promotion_type_id;')
        promotionlist = cursor.fetchall()
        cursor.execute("select * from tickets where is_fixed <> 1;")
        tickets = cursor.fetchall()
        ticket_ids = [entry['ticketid'] for entry in tickets if 'ticketid' in entry]
        cursor.execute("select * from promotion_types where promotion_type_id <> 1;")
        promotion_types = cursor.fetchall()
        return render_template('promotion_view.html', promotionlist = promotionlist, tickets = tickets, promotion_types = promotion_types, ticket_ids=ticket_ids)
    else:
        flash("Plase login in as staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))

def generate_coupon(length):
    """
    Generate a random coupon code of the given length
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@promotions.route('/promotions/add', methods=['POST'])
def promotion_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from promotion_types where promotion_type_id = %s and promotion_type_id <> 1", (request.form['promoType'], ))
        promo_type = cursor.fetchone()

        if promo_type['promotion_type_id'] == 1:
            now = datetime.now(timezone('Pacific/Auckland'))
            localdate = now.date()
            nextTuesday = localdate + timedelta(days=(8 - localdate.weekday()))
            return render_template('promotion_add_tuesday.html', nextTuesday = nextTuesday, promo_type = promo_type )
        else:
            return render_template('promotion_add.html', promo_type=promo_type)
        
    else:
        flash("Plase login in as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@promotions.route('/promotions/add_db', methods=['POST'])
def promotion_add_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from promotion_types where promotion_type_id = %s", (request.form['promoType'], ))
        promo_type = cursor.fetchone()

        if promo_type['promotion_type'] == 'tuesday':
            tueDate = request.form['tueDate']
            promotype = promo_type['promotion_type_id']
            # effective only in Tuesday daytime 7 am - 10 pm
            fromtime = tueDate + " " + "07:00:00"
            effective_date = datetime.strptime(fromtime, '%Y-%m-%d %H:%M:%S')
            totime = tueDate + " " + "19:00:00"
            expiration_date = datetime.strptime(totime, '%Y-%m-%d %H:%M:%S')

            title = request.form['title']
            descriptions = request.form['descriptions']
            details = request.form['details']
            image = request.form['image']

            # generate promocode - no need to use on Tuesday
            promocode = 't' + str(int(datetime.now().timestamp()))
            parameters = (title, descriptions, details, effective_date, expiration_date, image, promotype, promocode)

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # discount: discounted price, or non-price discount (other)
        else:
            title = request.form['title']
            descriptions = request.form['descriptions']
            details = request.form['details']
            effective_date = request.form['effective']
            expiration_date = request.form['expiration']
            image = request.form['image']
            promotype = promo_type['promotion_type_id']
            if promotype == 2:
                promocode = generate_coupon(20)
                # check if promocode exists
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('select distinct promotion_code from promotions;')
                promos = cursor.fetchall()
                promolist = [ sub['promotion_code'] for sub in promos ]
                count = 0
                while count in promolist and count < 100:
                    promocode = generate_coupon(20)
                    if count == 100:
                        flash("No available giftcards, please reach out to admin", "warning")
                        return redirect(url_for('promotions.promotion_view'))
                    else:
                        count = count + 1
            else:
                promocode = None
            
            parameters = (title, descriptions, details, effective_date, expiration_date, image, promotype, promocode)
        
        # sql and paramters
        
        sql = """
            INSERT INTO promotions (title, descriptions, details, effective_date, expiration_date, image, promotion_type_id, promotion_code)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, parameters)
        mysql.connection.commit()

        flash("Promotion is now added", "success")
        return redirect(url_for('promotions.promotion_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/delete')
def promotion_delete():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        promotionid = request.args.get('promotionid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM promotions WHERE promotionid = %s;", (promotionid,))
        mysql.connection.commit()
        flash(f"Promotion - id {promotionid} is now deleted", "success")
        return redirect(url_for('promotions.promotion_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/edit')
def promotion_edit():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        promotionid = request.args.get('promotionid')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        sql = """
            SELECT p.*, cast(p.effective_date as date) as effective 
            ,t.promotion_type, t.descriptions as type_desc
            FROM promotions p
            left join promotion_types t on p.promotion_type_id = t.promotion_type_id
            WHERE promotionid = %s;
            """
        cursor.execute(sql, (promotionid,))
        promotion = cursor.fetchone()
        promotype = promotion['promotion_type']
        if promotype == 'tuesday':
            cursor.execute("select * from tickets where is_fixed = 1")
            tueTicket = cursor.fetchone()
            if tueTicket:
                return render_template('promotion_edit_tuesday.html', promotion = promotion, tueTicket = tueTicket)
            else:
                flash("Tuesday Ticket is not available! Please set up Tuesday Ticket before editing this promotion", "warning")
                return redirect(url_for('promotions.promotion_view'))
        else:

            return render_template('promotion_edit.html', promotion = promotion)
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/update', methods=['POST'])
def promotion_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        # check if it is Tuesday datetime discount
        if request.form['promoType'] == '1':
            # tueDate = request.form['tueDate']
            # effective only in Tuesday daytime 7 am - 10 pm
            # fromtime = tueDate + " " + "07:00:00"
            # effective_date = datetime.strptime(fromtime, '%Y-%m-%d %H:%M:%S')
            # totime = tueDate + " " + "19:00:00"
            # expiration_date = datetime.strptime(totime, '%Y-%m-%d %H:%M:%S')

            promotionid = request.form['promotionid']
            title = request.form['title']
            descriptions = request.form['descriptions']
            details = request.form['details']
            image = request.form['image']
            protype = request.form['promoType']

            ticketid = request.form['ticketid']
            price = request.form['price']

            if ticketid == None or price == None or ticketid == '' or price == '':
                flash("Tuesday Ticket is not available! Please set up Tuesday Ticket before editing this promotion", "warning")
                return redirect(url_for('promotions.promotion_view'))
            else:
                # update Tuesday discount price
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE tickets SET price = %s WHERE ticketid = %s and is_fixed = 1", (price, ticketid))
                # only commit if the promotion is updated below 
            
                parameters = (title, descriptions, details, image, protype, promotionid)
                sql = """
                    UPDATE promotions
                    SET title = %s, descriptions = %s, details = %s, image = %s, promotion_type_id = %s 
                    WHERE promotionid = %s
                """
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sql, parameters)
                mysql.connection.commit()

        else:
            promotionid = request.form['promotionid']
            title = request.form['title']
            descriptions = request.form['descriptions']
            details = request.form['details']
            effective_date = request.form['effective']
            expiration_date = request.form['expiration']
            image = request.form['image']
            protype = request.form['promoType']
        
            parameters = (title, descriptions, details, effective_date, expiration_date, image, protype, promotionid)
            sql = """
                UPDATE promotions
                SET title = %s, descriptions = %s, details = %s, effective_date = %s, expiration_date = %s, image = %s, promotion_type_id = %s 
                WHERE promotionid = %s
            """
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
        
        flash(f"Promotion - id {promotionid} is now updated", "success")
        return redirect(url_for('promotions.promotion_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/ticket')
def promotion_ticket_view():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        # get local current
        now = datetime.now(timezone('Pacific/Auckland'))
        localdate = now.date()
        # get all tickets
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from tickets;")
        tickets = cursor.fetchall()
        ticket_ids = [entry['ticketid'] for entry in tickets if 'ticketid' in entry]
        # get all ticket promotions
        sql = """
                select tpid
                    ,t.ticketid
                    ,t.ticket_type
                    ,t.price as standard_price
                    ,case when is_percentage = 0 then tp.discounted_price else t.price - (t.price * convert(tp.discount_percentage, decimal(5,2))/100) end as discounted_price
                    ,case when is_percentage = 1 then tp.discount_percentage else (t.price - convert(tp.discounted_price, decimal(5,2)))/t.price * 100 end as discount_percentage
                    ,tp.promotionid
                    ,tp.latest_version
                    ,case when tp.latest_version = 1 then 'Latest' else 'Historical' end as latest
                    ,p.title
                    ,p.effective_date
                    ,p.expiration_date
                    ,cast(p.effective_date as date) as effective
                    ,tp.is_percentage
                from ticket_promotion tp
                left join tickets t on t.ticketid = tp.ticketid
                left join promotions p on p.promotionid = tp.promotionid
                order by tp.latest_version desc, tpid desc, p.effective_date desc, p.expiration_date desc
            """
        cursor.execute(sql)
        history = cursor.fetchall()
        return render_template('promotion_ticket_view.html', tickets = tickets, history = history, localdate = localdate, ticket_ids=ticket_ids)
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

# @promotions.route('/promotions/ticket/add', methods=['POST'])
# def promotion_ticket_add():
#     if 'loggedin' in session and session['role'] in ('manager', 'admin'):
#         now = datetime.now(timezone('Pacific/Auckland'))
#         localdate = now.strftime("%Y-%m-%d")
#         ticketid = request.form["ticketType"]
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # get ticket info
#         cursor.execute("select * from tickets where ticketid = %s;", (ticketid, ))
#         ticket = cursor.fetchone()
#         # get valid promotions
#         cursor.execute("select * from promotions where expiration_date >= %s and promotion_type = 'price' ;", (localdate, ))
#         promotions = cursor.fetchall()
#         return render_template('promotion_ticket_add_copy.html', ticket = ticket, promotions = promotions)
#     else:
#         flash("Plase login as manager or admin", "warning")
#         return redirect(url_for('staff_login.stafflogin'))

#------------------------------------------select 'All ticket types' or 'individual ticket type'--------------------------------------
@promotions.route('/promotions/ticket/add', methods=['POST'])
def promotion_ticket_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        now = datetime.now(timezone('Pacific/Auckland'))
        localdate = now.strftime("%Y-%m-%d %H:%M:%S")
        ticket_ids_str =request.form.getlist("ticketType")
        ticket_ids = eval(ticket_ids_str[0])
        
        # user choose 'All types' which id is a list, if they chose individual type, id is an int. It will render different pages.
        if isinstance(ticket_ids, list):
            # get valid promotions
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from promotions where expiration_date >= %s and promotion_type_id = 2 and is_active = 1;", (localdate, ))
            promotions = cursor.fetchall()
            return render_template('promotion_ticket_add_all.html',ticket_ids=ticket_ids, promotions = promotions)
        elif isinstance(ticket_ids, int):
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # get ticket info
            cursor.execute("select * from tickets where ticketid = %s and is_fixed = 0;", (ticket_ids,))
            ticket = cursor.fetchone()
            # get valid promotions
            cursor.execute("select * from promotions where expiration_date >= %s and promotion_type_id = 2 and is_active = 1;", (localdate, ))
            promotions = cursor.fetchall()
            return render_template('promotion_ticket_add.html', ticket = ticket, promotions = promotions)
        else:
            flash("No ticket id received", "warning")
            return redirect(url_for('promotions.promotion_ticket_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
#---------------------------after user chose 'All ticket types'---------------------------------   
# add ticket promotion to database via updating dicounted_price
@promotions.route('/promotions/ticket/add_disc_db', methods=['POST'])
def promotion_ticket_add_disc_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):           
        #Get these values which user inputed
        discount = request.form['disc']
        promotionid = request.form['promotionid']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # deactive historical promotion
        sql_deactivate = """
            UPDATE ticket_promotion SET latest_version = 0 
            WHERE ticketid in (
                SELECT DISTINCT ticketid FROM tickets
                WHERE is_fixed = 0
            )
            """
        cursor.execute(sql_deactivate)

        # update new promotion to the selected ticket

        # if user selected discounted price, discounted price = discount, percentage = (price - discount)/price
        if request.form['discountSelected'] == "0":
            sql = """
                INSERT INTO ticket_promotion (original_price, discounted_price, discount_percentage, ticketid, promotionid, is_percentage)
                SELECT price, %s, (price - convert(%s, decimal(5,2)))/price * 100, ticketid, %s, 0
                FROM tickets
                WHERE is_fixed = 0
                """
            parameters = (discount, discount, promotionid)
        # if user selected percentage, percentage = discount, discounted price = price - price * discount
        else:
            sql = """
                INSERT INTO ticket_promotion (original_price, discounted_price, discount_percentage, ticketid, promotionid, is_percentage)
                SELECT price,  price - (price * convert(%s, decimal(5,2))/100), %s, ticketid, %s, 1
                FROM tickets
                WHERE is_fixed = 0
                """
            parameters = (discount, discount, promotionid)

        cursor.execute(sql, parameters)
        # commit changes
        mysql.connection.commit()
        flash(f"Ticket prices for all ticket types are now updated for promotion # {promotionid}", "success")
        return redirect(url_for('ticket_price.manage_ticket_prices'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))



#-----------------------------select 'All ticket types' end----------------------------------------

#---------------------------after user select one signle ticket type---------------------------------   
# add ticket promotion to database
@promotions.route('/promotions/ticket/add_db', methods=['POST'])
def promotion_ticket_add_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        ticketid = request.form['ticketid']
        promotionid = request.form['promotionid']
        tickettype = request.form['tickettype']
        currentprice = request.form['currentprice']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # deactive historical promotion
        cursor.execute("UPDATE ticket_promotion SET latest_version = 0 WHERE ticketid = %s;", (ticketid,))

        # update new promotion to the selected ticket
        if request.form['discountSelected'] == "0":
            sql = """
                INSERT INTO ticket_promotion (original_price, discounted_price, discount_percentage, ticketid, promotionid, is_percentage)
                VALUES
                (%s, %s, NULL, %s, %s, 0)
                """
            discount = request.form['disc']
            parameters = (currentprice, discount, ticketid, promotionid)
        else:
            sql = """
                INSERT INTO ticket_promotion (original_price, discounted_price, discount_percentage, ticketid, promotionid, is_percentage)
                VALUES
                (%s, NULL, %s, %s, %s, 1)
                """
            percentage = request.form['perc']
            parameters = (currentprice, percentage, ticketid, promotionid)
        cursor.execute(sql, parameters)

        # commit changes
        mysql.connection.commit()

        flash(f"Ticket price for {tickettype} is now updated for promotion # {promotionid}", "success")
        return redirect(url_for('promotions.promotion_ticket_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))
#--------------------------- select one signle ticket type and update end--------------------------------- 

@promotions.route('/promotions/ticket/delete', methods=['GET'])
def promotion_ticket_delete():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        tpid = request.args.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM ticket_promotion WHERE tpid = %s;", (tpid,))
        mysql.connection.commit()
        flash(f"Ticket-Promotion #{tpid} is now deleted", "success")
        return redirect(url_for('promotions.promotion_ticket_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/ticket/edit', methods=['GET'])
def promotion_ticket_edit():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        now = datetime.now(timezone('Pacific/Auckland'))
        localdate = now.strftime("%Y-%m-%d")
        ticketid = request.args.get('ticketid')
        tpid = request.args.get('tpid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # get ticket info
        cursor.execute("select * from tickets where ticketid = %s;", (ticketid, ))
        ticket = cursor.fetchone()
        # get valid promotions
        cursor.execute("select * from promotions where expiration_date >= %s and promotion_type_id = 2 ;", (localdate, ))
        promotions = cursor.fetchall()
        # get current version
        cursor.execute("""select tp.tpid, tp.is_percentage
                       , case when is_percentage = 0 then tp.discounted_price else t.price - (t.price * convert(tp.discount_percentage, decimal(5,2))/100) end as discounted_price
                    ,case when is_percentage = 1 then tp.discount_percentage else (t.price - convert(tp.discounted_price, decimal(5,2)))/t.price * 100 end as discount_percentage
                    from ticket_promotion tp  
                    left join tickets t on t.ticketid = tp.ticketid   
                    where tpid = %s;""", (tpid, ))
        currentversion = cursor.fetchone()
        return render_template('promotion_ticket_edit.html', ticket = ticket, promotions = promotions, currentversion = currentversion)
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@promotions.route('/promotions/ticket/update', methods=['POST'])
def promotion_ticket_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        tpid = request.form['tpid']
        promotionid = request.form['promotionid']
        
        tickettype = request.form['tickettype']
        currentprice = request.form['currentprice']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # insert new version
        if request.form['discountSelected'] == "0": 
            sql = """
                UPDATE ticket_promotion
                SET promotionid = %s, discount_percentage = NULL, discounted_price = %s, original_price = %s, is_percentage = 0
                WHERE tpid = %s;
            """
            discount = request.form['disc']
            parameters = (promotionid, discount, currentprice, tpid )
        else:
            sql = """
                UPDATE ticket_promotion
                SET promotionid = %s, discount_percentage = %s, discounted_price = NULL, original_price = %s, is_percentage = 1
                WHERE tpid = %s;
            """
            percentage = request.form['perc']
            parameters = (promotionid, percentage, currentprice, tpid )

        cursor.execute(sql, parameters)
        mysql.connection.commit()
        flash(f"Ticket {tickettype} is now updated to promotion # {promotionid}", "success")
        return redirect(url_for('promotions.promotion_ticket_view'))
    else:
        flash("Plase login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

# update promotion status - active or inactive (enabled or disabled)
@promotions.route('/promotions/status_update', methods=['POST'])
def promotion_status():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        data = request.get_json()
        promotionid = data['promotionid']
        status = data['is_active']
        if status == True:
            is_active = 1
            is_enable = "Enabled"
        else:
            is_active = 0
            is_enable = "Disabled"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE promotions SET is_active = %s WHERE promotionid = %s;", (is_active,promotionid ))
        mysql.connection.commit()

        return jsonify(updatestatus=1, isenable=is_enable)
    else:
        return jsonify(updatestatus=0)

@promotions.route('/promotions/validation', methods=['POST'])
def promotion_validation():
    data  = request.get_json()
    promocode = data['promocode']
    now = datetime.now(timezone('Pacific/Auckland'))
    # current_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    # promotion based on session datetime 
    if promocode != '':
        session_datetime = data['session_datetime']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from promotions where promotion_code = %s and effective_date <= %s and expiration_date >= %s", (promocode, session_datetime, session_datetime))
        result = cursor.fetchone()
        if result:
            sql = """
                select tpid
                    ,t.ticketid
                    ,t.ticket_type
                    ,t.price as standard_price
                    ,case when is_percentage = 0 then tp.discounted_price else t.price - (t.price * convert(tp.discount_percentage, decimal(5,2))/100) end as discounted_price
                    ,case when is_percentage = 1 then tp.discount_percentage else (t.price - convert(tp.discounted_price, decimal(5,2)))/t.price * 100 end as discount_percentage
                    ,tp.promotionid
                from ticket_promotion tp
                left join tickets t on t.ticketid = tp.ticketid 
                where promotionid = %s
                """
            cursor.execute(sql, (result['promotionid'], ))
            ticketpromo = cursor.fetchall()
            if ticketpromo:
                tpdict = {}
                for elem in ticketpromo:
                    tpdict[elem['ticketid']] = elem['discounted_price']
                return jsonify(promovalid="true", tpdict=tpdict)
            else:
                return jsonify(promovalid="false")

        return jsonify(promovalid="false")
        
    else: 
        return jsonify(promovalid="false")

