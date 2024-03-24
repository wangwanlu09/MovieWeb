
from app import mysql
from flask import Blueprint, render_template,request, url_for, redirect, session,flash,get_flashed_messages
import MySQLdb.cursors
from datetime import date, datetime, timedelta
import bcrypt
from password_strength import PasswordPolicy
from password_strength import PasswordStats

customer_login = Blueprint('customer_login', __name__)


@customer_login.route('/customerlogin')
def customerlogin():
    return render_template('login.html')

@customer_login.route('/customer_login_verify', methods=['GET', 'POST'])
def customer_login_verify():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: #user need to enter these information to login
        username = request.form['username'].strip() 
        password = request.form['password'].strip()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""select a.accountid, a.username, a.password, r.role
            ,c.is_active
            from accounts a
            left join roles r on r.roleid = a.roleid 
            left join customers c on c.accountid = a.accountid
            where a.roleid = 4
            and a.username = %s ;""", (username,))
        account = cursor.fetchone()# get the account information for this unique username

        if account is not None:
            if account['is_active'] == 0 or account['is_active'] == '0':
                flash('Not an active account', "warning")
                return redirect(url_for('customer_login.customerlogin'))
            if bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8')): #check passwords if match
                session['loggedin'] = True
                session['accountid'] = account['accountid']  
                session['username'] = account['username']
                session['role'] = account['role']
                if session['role']  == "customer":  # verify if this is a customer account!
                    if 'booking_url' in session:
                        session.pop('booking_url', None)
                        return redirect(url_for('payments.payment_booking'))
                    elif 'url' in session:
                        previouspage = session['url']
                        session.pop('url', None)
                        return redirect(previouspage)
                    else:
                        return redirect(url_for('customer_login.my_dashboard'))
                else:
                    flash('Invalid account', "warning") 
                    return redirect(url_for('customer_login.customerlogin'))   
            else: # if password  is not correct
                flash('Wrong password', "warning")    
                return redirect(url_for('customer_login.customerlogin'))
        else:   
            flash('Wrong username', "warning")
            return redirect(url_for('customer_login.customerlogin'))
    else:
        return redirect(url_for('customer_login.customerlogin'))
 
@customer_login.route('/my_dashboard')
def my_dashboard():
    if 'loggedin' in session:
        if session['role']  == "customer":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from customers where accountid = %s", (session['accountid'],))
            firstname = cursor.fetchone()


            # booking history
            sql_movies = """
                select 
                m.title
                ,c.name
                ,b.booking_date
                ,s.session_date
                ,TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS sessiontime
                ,timestamp(s.session_date, st.sessiontime) as session_datetime
                from bookings b
                left join customers cu on cu.customerid = b.customerid
                left join sessions s on s.sessionid = b.sessionid
                left join sessiontime st on st.sessiontime_id = s.sessiontime_id
                left join cinemas c on c.cinemaid = st.cinemaid
                left join movies m on m.movieid = s.movieid
                where cu.accountid = %s
                order by b.booking_date desc
                limit 1
            """
            cursor.execute(sql_movies, (session['accountid'],))
            booking = cursor.fetchone()

            # giftcard history
            sql_gc = """
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
            where c.accountid = %s
            order by p.payment_date desc
            limit 1
            """        
            cursor.execute(sql_gc,  (session['accountid'],))
            giftcard = cursor.fetchone()

            return render_template('dashboard_customer.html', firstname = firstname, booking=booking, giftcard=giftcard)
        
    
    return redirect(url_for('customer_login.customerlogin'))


@customer_login.route("/customer_profile", methods =['GET']) #click personal info box and user will enter this url
def customer_profile():
    if 'loggedin' in session:
        if session['role']  == "customer":
            accountid = session['accountid']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""SELECT a.accountid, a.username, a.password, a.roleid, r.role
                            FROM accounts a
                            LEFT JOIN roles r ON a.roleid = r.roleid where accountid = %s;""", (accountid,))
            account = cursor.fetchone()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from customers where accountid = %s;", (accountid,))
            customer = cursor.fetchone()
            return render_template("dashprofile_customer.html",account=account,customer=customer)

    return redirect(url_for('customer_login.customerlogin'))
    

@customer_login.route("/customer_profile_update", methods =['GET', 'POST']) #click edit profile button and will direct to this route
def customer_profile_update():
    if 'loggedin' in session:
        if session['role']  == "customer":
            if request.method == 'GET':
                accountid = session['accountid']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT a.accountid, a.username, a.password, a.roleid, r.role\
                            FROM accounts a\
                            LEFT JOIN roles r ON a.roleid = r.roleid where accountid = %s;", (accountid,))
                account = cursor.fetchone() 
                print("account in update",account)
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM customers WHERE accountid = %s;", (accountid, ))
                customer= cursor.fetchone() # get customer table info to display, which will be edit later.
                print("customer in update",customer)
                return render_template("manage_profile_customer.html",account=account,customer=customer)  
            else:
                Fname = request.form['firstName']
                Lname = request.form['lastName']
                phone = request.form['phone']
                accountid = session['accountid']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update user table to database
                cursor.execute('UPDATE customers SET firstname =%s,lastname=%s,phone=%s WHERE (accountid =%s)', (Fname,Lname,phone,(accountid,)))
                mysql.connection.commit() # if there is already a user_id after registration, then just update customer data.
                flash(" Profile updated successfully!", "success")
                return redirect(url_for('customer_login.customer_profile'))
    flash("Please log in", "warning")
    return redirect(url_for('customer_login.customerlogin'))

policy = PasswordPolicy.from_names(
    length=8,      # minimum length: 8 characters
    uppercase=1,   # require at least 1 uppercase letter
    numbers=1,     # require at least 1 digit
    strength= 0.2,   # require at least 0.5 with its entropy bits
)

@customer_login.route("/customer_change_pw", methods =['GET', 'POST']) #click edit profile button and will direct to this route
def customer_change_pw():    
    if 'loggedin' in session and session['role'] == 'customer':
        accountid = session['accountid']
        if request.method == 'POST':
            old_password = request.form['oldPassword']
            new_password = request.form['newPassword']
            confirm_pass = request.form['confirmPassword']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts where accountid =%s;',(accountid,))
            account = cursor.fetchone()  # get the old password from accounts
            stats = PasswordStats(new_password)
            checkpolicy = policy.test(new_password)

            if account and bcrypt.checkpw(old_password.encode('utf-8'), account['password'].encode('utf-8')):  # check if the right old password
                if checkpolicy and stats.strength() < 0.4:
                    flash("Password not strong enough.Avoid consecutive characters and easily guessed words.","warning")
                    return redirect(url_for('customer_login.customer_profile'))
                elif new_password == confirm_pass:
                    Newpassword=bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()) #hash the new password and put it into database
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE accounts SET  password =% s WHERE accountid =% s', (Newpassword, accountid))
                    mysql.connection.commit()
                    # log out
                    session.pop('loggedin', None)
                    session.pop('username', None)
                    session.pop('role', None)
                    session.pop('accountid', None)
                    # ask to log in again with new password
                    flash("Password updated successfully! Please log in with the new password", "success")
                    return redirect(url_for('customer_login.customerlogin'))
                else:
                    flash("New password and confirm password do not match.", "warning")
                    return redirect(url_for('customer_login.customer_profile'))
            else:
                flash("Invalid old password.", "warnning")
                return redirect(url_for('customer_login.customer_profile'))
        else:
            flash("Please fill all the blanks.", "warnning")
            return redirect(url_for('customer_login.customer_profile'))
    else:
        return redirect(url_for('customer_login.customerlogin'))


