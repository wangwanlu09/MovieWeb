from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, jsonify
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone
import random, string

giftcards = Blueprint('giftcards', __name__)

@giftcards.route('/giftcard')
def giftcard_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from giftcard_types;")
    giftcards = cursor.fetchall()
    return render_template('giftcard_home.html', giftcards=giftcards)

@giftcards.route('/giftcard/buy', methods=['GET'])
def giftcard_buy():
    giftcard_type_id = request.args.get('giftcard_type_id')
    if giftcard_type_id == '' or giftcard_type_id == None:
        giftcard_type_id = 1
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from giftcard_types where giftcard_type_id = %s ;", (giftcard_type_id, ))
    giftcard = cursor.fetchone()    
    return render_template('giftcard_buy.html', giftcard = giftcard)

@giftcards.route('/giftcard/checklogin', methods=['POST', 'GET'])
def giftcard_checklogin():
    session['url'] = request.referrer
    return redirect (url_for('customer_login.customerlogin'))

@giftcards.route('/giftcard/validation', methods=['POST'])
def giftcard_validation():
    if request.method == "POST":
        giftcard_number = request.get_json()['number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            with cte_booking as (
                select b.giftcardid, sum(b.giftcard_deducted) as gcdeducted
                from payment p
                left join bookings b on b.bookingid = p.bookingid
                where p.payment_type = 'booking'
                and b.giftcardid is not NULL
                group by b.giftcardid
            )
            select g.* ,
            case when gcdeducted is null then g.giftcard_value else
                g.giftcard_value - cb.gcdeducted end as balance
            from giftcards g
            left join cte_booking cb on g.giftcardid = cb.giftcardid
            where giftcard_number = %s
            """
        cursor.execute(sql, (giftcard_number, ))
        result = cursor.fetchone()
        if result == None:
            return jsonify({"giftcard_exists": "false"})
        else:
            # balance query:
            # if balance = 0, invalid giftcard
            # if balance > 0, return balance amount:
            if result['balance'] > 0:
                return jsonify(giftcard_exists="true", balance = result['balance'])
            else:
                return jsonify({"giftcard_exists": "false"})
    else:
        return redirect(url_for('giftcards.giftcard_home'))

@giftcards.route('/giftcard/payment', methods=['POST'])
def giftcard_payment():
    if 'loggedin' in session and session['role'] == 'customer':
        if request.method == "POST": 
            amount = request.form['amountSelect']
            quantity = request.form['quantitySelect']
            giftcard_type_id = request.form['giftcard_type_id']
            total = int(amount) * int(quantity)
            today = datetime.now(timezone('Pacific/Auckland'))
            currentmonth = today.strftime('%Y-%m')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from giftcard_types where giftcard_type_id = %s ;", (giftcard_type_id, ))
            giftcard = cursor.fetchone()
            return render_template('giftcard_payment.html', giftcard = giftcard, amount = amount, quantity = quantity, giftcard_type_id = giftcard_type_id, total = total, currentmonth = currentmonth)
        else:
            return redirect(url_for('giftcards.giftcard_home'))
    else:
        flash("Please log in as customer to purchase giftcards", "warning")
        return redirect (url_for('customer_login.customerlogin'))


def generate_coupon(length):
    """
    Generate a random coupon code of the given length
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@giftcards.route('/giftcard/payment/update', methods=['POST'])
def giftcard_payment_update():
    if 'loggedin' in session and session['role'] == 'customer':
        if request.method == "POST": 
            gcamount = request.form['amount']
            quantity = request.form['quantity']
            giftcard_type_id = request.form['giftcard_type_id'] 
            total = request.form['total']

            now = datetime.now(timezone('Pacific/Auckland'))
            now_date = now.strftime('%Y-%m-%d')
            now_time = now.strftime('%H:%M:%S')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # create payment 
            sql_py = """
                INSERT INTO payment (amount, payment_date, payment_time, payment_type, customerid)
                SELECT %s, %s, %s, 'giftcard', c.customerid
                FROM customers c
                LEFT JOIN accounts a on a.accountid = c.accountid
                WHERE c.accountid = %s;
                """
            parameters_py = (total, now_date, now_time, session['accountid'])
            cursor.execute(sql_py, parameters_py)
            # get paymentid
            paymentid = cursor.lastrowid

            # sql to create giftcards in database
            sql_gc = """
                INSERT INTO giftcards (giftcard_number, giftcard_value, giftcard_type_id, customerid)
                SELECT %s, %s, %s, c.customerid
                FROM customers c
                LEFT JOIN accounts a on a.accountid = c.accountid
                WHERE c.accountid = %s;
                """
            
            # get all the giftcard number from database
            cursor.execute('select distinct giftcard_number from giftcards;')
            giftcards = cursor.fetchall()
            gclist = [ sub['giftcard_number'] for sub in giftcards ]
            # generage giftcard numbers and insert to giftcards
            for i in range(int(quantity)):
                gcnumbers = (generate_coupon(16))
                count = 0
                while gcnumbers in gclist and count < 100:
                    gcnumbers = (generate_coupon(16))
                    if count == 100:
                        flash("No available giftcards, please contact us", "warning")
                        return redirect(url_for('giftcards.giftcard_home'))
                    else:
                        count = count + 1
                
                parameters_gc = (gcnumbers, gcamount, giftcard_type_id, session['accountid'])

                # generate giftcards
                cursor.execute(sql_gc, parameters_gc )
                giftcardid = cursor.lastrowid

                # link giftcard and payment
                cursor.execute("INSERT INTO giftcard_payment (giftcardid, paymentid) VALUES (%s, %s)", (giftcardid, paymentid))

            # commit changes
            mysql.connection.commit()

            # return to giftcard purchase history page
            flash("Purchase success", "success")
            return redirect(url_for('giftcards.giftcard_customer')) 
            

        else:
            return redirect(url_for('giftcards.giftcard_home'))
    else:
        flash("Please log in as customer to purchase giftcards", "warning")
        return redirect (url_for('customer_login.customerlogin'))

@giftcards.route('/customer/giftcards')
def giftcard_customer():
    if 'loggedin' in session and session['role'] == 'customer':
        sql = """
            with cte_booking as (
                select b.giftcardid, sum(b.giftcard_deducted) as gcdeducted
                from payment p
                left join bookings b on b.bookingid = p.bookingid
                where p.payment_type = 'booking'
                and b.giftcardid is not NULL
                group by b.giftcardid
            )
            select g.*, gt.giftcard_name, p.payment_date, 
            case when gcdeducted is null then g.giftcard_value else
                g.giftcard_value - gcdeducted end as balance
            from giftcards g
            left join giftcard_types gt on gt.giftcard_type_id = g.giftcard_type_id
            left join customers c on c.customerid = g.customerid
            left join accounts a on c.accountid = a.accountid
            left join cte_booking cb on g.giftcardid = cb.giftcardid
            left join giftcard_payment gp on g.giftcardid = gp.giftcardid
            left join payment p on p.paymentid = gp.paymentid
            where c.accountid = %s;
            """
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, (session['accountid'], ))
        giftcards = cursor.fetchall()
        return render_template('giftcard_customer.html', giftcards = giftcards)
    else:
        flash("Pleae log in", "warning")
        return redirect (url_for('customer_login.customerlogin'))

@giftcards.route('/giftcard/preview')
def giftcard_preview():
    if 'loggedin' in session and session['role'] == 'customer':
        giftcardid = request.args.get('giftcardid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                select g.*, gt.giftcard_name, gt.image 
                from giftcards g
                left join giftcard_types gt on gt.giftcard_type_id = g.giftcard_type_id
                where g.giftcardid = %s
            """
        cursor.execute(sql, (giftcardid, ))
        giftcard = cursor.fetchone()
        return render_template('giftcard_print.html', giftcard = giftcard)
    else:
        flash("Pleae log in", "warning")
        return redirect (url_for('customer_login.customerlogin'))

@giftcards.route('/giftcard/balance')
def giftcard_balance():
    return render_template('giftcard_balance.html')