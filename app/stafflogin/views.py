from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, jsonify
import MySQLdb.cursors
import bcrypt
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from datetime import date, datetime, timedelta, time
from pytz import timezone

staff_login = Blueprint('staff_login', __name__)

# http://127.0.0.1:5000/stafflogin
@staff_login.route('/stafflogin')
def stafflogin():
    return render_template('login_staff.html')

# http://127.0.0.1:5000/staff/dashboard
@staff_login.route('/staff/check', methods=['GET', 'POST'])
def staffcheck():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        user_password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            select a.accountid, username, password, role
            ,s.is_active as is_active
            from accounts a
            left join roles r on r.roleid = a.roleid 
            left join staff s on s.accountid = a.accountid
            where a.roleid <> 4
            and a.username = %s;
            """
        cursor.execute(sql, (username,))
        account = cursor.fetchone()

        if account is not None:
            if account['is_active'] == 0 or account['is_active'] == '0':
                flash('Not an active account', "warning")
                return redirect(url_for('staff_login.stafflogin'))
            password = account['password']
            if bcrypt.checkpw(user_password.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['accountid'] = account['accountid']
                session['username'] = account['username']
                session['role'] = account['role']
                # Redirect to dashboard according to roles
                if session['role'] == 'staff':
                    return redirect(url_for('staff_login.staffdashboard'))
                elif session['role'] == 'manager':
                    return redirect(url_for('staff_login.managerdashboard'))
                elif session['role'] == 'admin':
                    return redirect(url_for('staff_login.admindashboard'))
                else:
                    flash('Not a valid staff account', "warning")
                    return render_template('login_staff.html')
            else:
                #password incorrect
                flash('Wrong password', "warning")
                return render_template('login_staff.html')
        else:
            # Account doesnt exist or username incorrect
            flash('Wrong username', "warning")
            return render_template('login_staff.html')
    flash("Please log in as staff, manager or admin", "warning")
    return render_template('login_staff.html')

@staff_login.route('/staff/dashboard')
def staffdashboard():
    if 'loggedin' in session and session['role'] == 'staff':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s", (session['accountid'],))
        firstname = cursor.fetchone()

        # upcoming session
        now = datetime.now(timezone('Pacific/Auckland'))
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        sql = """
            SELECT 
                c.*,
                s.*,
                TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours
                ,st.sessiontime
                ,m.title
            FROM
                cinemas c
            JOIN
                sessiontime st ON c.cinemaid = st.cinemaid
            JOIN
                sessions s ON st.sessiontime_id = s.sessiontime_id
            LEFT JOIN movies m ON s.movieid = m.movieid
            WHERE s.session_date = %s
            AND st.sessiontime > %s
            ORDER BY s.session_date, st.sessiontime, c.cinemaid
            LIMIT 1
        """
        cursor.execute(sql, (current_date, current_time))
        latestsession = cursor.fetchone()
        return render_template('dashboard_staff.html', firstname = firstname, latestsession=latestsession)
    else:
        flash("Please log in as staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@staff_login.route('/manager/dashboard')
def managerdashboard():
    if 'loggedin' in session and session['role'] == 'manager':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s", (session['accountid'],))
        firstname = cursor.fetchone()
        # upcoming session
        now = datetime.now(timezone('Pacific/Auckland'))
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        sql = """
            SELECT 
                c.*,
                s.*,
                TIME_FORMAT(st.sessiontime, '%%h:%%i %%p') AS session12hours
                ,st.sessiontime
                ,m.title
            FROM
                cinemas c
            JOIN
                sessiontime st ON c.cinemaid = st.cinemaid
            JOIN
                sessions s ON st.sessiontime_id = s.sessiontime_id
            LEFT JOIN movies m ON s.movieid = m.movieid
            WHERE s.session_date = %s
            AND st.sessiontime > %s
            ORDER BY s.session_date, st.sessiontime, c.cinemaid
            LIMIT 1
        """
        cursor.execute(sql, (current_date, current_time))
        latestsession = cursor.fetchone()

        today = datetime.now(timezone('Pacific/Auckland'))
        date30 = today + timedelta(days=-30)
        parameters_date = (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

        # new customer counts
        cursor.execute("select count(customerid) as newcustomers from customers where join_date between %s and %s", parameters_date)
        newcustomers = cursor.fetchone()['newcustomers']

        # bookings made
        cursor.execute("select count(bookingid) as countbookings,  COALESCE(SUM(total_amount),0) as ticketsales_amt from bookings where booking_date between %s and %s", parameters_date)
        bookings =  cursor.fetchone()
        countbookings = bookings['countbookings']
        ticketsales_amt = bookings['ticketsales_amt']
        
        return render_template('dashboard_manager.html', firstname = firstname, latestsession=latestsession, newcustomers=newcustomers, countbookings=countbookings, ticketsales_amt=ticketsales_amt)
    else:
        flash("Please log in as manager", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@staff_login.route('/admin/dashboard')
def admindashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s", (session['accountid'],))
        firstname = cursor.fetchone()

        today = datetime.now(timezone('Pacific/Auckland'))
        date30 = today + timedelta(days=-30)
        parameters_date = (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

        # new customer counts
        cursor.execute("select count(customerid) as newcustomers from customers where join_date between %s and %s", parameters_date)
        newcustomers = cursor.fetchone()['newcustomers']

        # bookings made
        cursor.execute("select count(bookingid) as countbookings,  COALESCE(SUM(total_amount),0) as ticketsales_amt from bookings where booking_date between %s and %s", parameters_date)
        bookings =  cursor.fetchone()
        countbookings = bookings['countbookings']
        ticketsales_amt = bookings['ticketsales_amt']

        return render_template('dashboard_admin.html', firstname = firstname, newcustomers=newcustomers, countbookings=countbookings, ticketsales_amt=ticketsales_amt)
    else:
        flash("Please log in as admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

# http://127.0.0.1:5000/staff/profile
@staff_login.route('/staff/profile')
def staff_profile():
    if 'loggedin' in session and session['role'] == 'staff':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s;", (session['accountid'],))
        account = cursor.fetchone()
        return render_template('dashprofile_staff.html', account=account)
    else:
        return redirect(url_for('staff_login.stafflogin'))

# http://127.0.0.1:5000/manager/profile
@staff_login.route('/manager/profile')
def manager_profile():
    if 'loggedin' in session and session['role'] == 'manager':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s;", (session['accountid'],))
        account = cursor.fetchone()
        return render_template('dashprofile_manager.html', account=account)
    else:
        flash("Please log in as manager", "warning")
        return redirect(url_for('staff_login.stafflogin'))

# http://127.0.0.1:5000/manager/profile
@staff_login.route('/admin/profile')
def admin_profile():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from staff where accountid = %s;", (session['accountid'],))
        account = cursor.fetchone()
        return render_template('dashprofile_admin.html', account=account)
    else:
        flash("Please log in as admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@staff_login.route('/validate/oldpw', methods=['POST'])
def staff_oldpw():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from accounts where accountid = %s;", (session['accountid'],))
    account = cursor.fetchone()
    old_password = request.get_json()['oldpw']
    if account and bcrypt.checkpw(old_password.encode('utf-8'), account['password'].encode('utf-8')):
        return jsonify(validatepw="true")
    else:
        return jsonify(validatepw="false")

policy = PasswordPolicy.from_names(
    length=8,      # minimum length: 8 characters
    uppercase=1,   # require at least 1 uppercase letter
    numbers=1,     # require at least 1 digit
    strength= 0.5,   # require at least 0.5 with its entropy bits
)

@staff_login.route('/staff/change/password', methods=['POST'])
def staff_changepw():
    if 'loggedin' in session:
        accountid = session['accountid']
        if request.method == 'POST':
            old_password = request.form['oldPassword']
            new_password = request.form['newPassword']
            confirm_pass = request.form['confirmPassword']
            stats = PasswordStats(new_password)
            checkpolicy = policy.test(new_password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts where accountid =%s;',(accountid,))
            account = cursor.fetchone()  # get the old password from accounts

            if account and bcrypt.checkpw(old_password.encode('utf-8'), account['password'].encode('utf-8')):  # check if the right old password
                if checkpolicy and stats.strength() < 0.5:
                        flash("Password not strong enough.Avoid consecutive characters and easily guessed words.","warning")
                        if session['role'] == 'staff':
                            return redirect(url_for('staff_login.staff_profile'))
                        elif session['role'] == 'manager':
                            return redirect(url_for('staff_login.manager_profile'))
                        elif session['role'] == 'admin':
                            return redirect(url_for('staff_login.admin_profile'))
                        else:
                            return redirect(url_for('staff_login.stafflogin'))
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
                    flash("Password updated successfully! Please log in again", "success")
                    return redirect(url_for('staff_login.stafflogin'))

                else:
                    flash("New password and confirm password do not match.", "warning")
                    if session['role'] == 'staff':
                        return redirect(url_for('staff_login.staff_profile'))
                    elif session['role'] == 'manager':
                        return redirect(url_for('staff_login.manager_profile'))
                    elif session['role'] == 'admin':
                        return redirect(url_for('staff_login.admin_profile'))
                    else:
                        return redirect(url_for('staff_login.stafflogin'))
            else:
                flash("Invalid old password.", "warnning")
                return redirect(url_for('staff_login.staff_profile'))
        else:
            flash("Please fill all the blanks.", "warnning")
            return redirect(url_for('staff_login.staff_profile'))
    else:
        flash("Please log in ", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@staff_login.route('/staff/profile/edit')
def staff_profile_edit():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):

        sql = "select * from staff where accountid = %s;"
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, (session['accountid'], ))
        account = cursor.fetchone() 
        return render_template('manage_profile_staff.html', account = account)
    
    flash("Please log in ", "warning")
    return redirect(url_for('staff_login.stafflogin'))


@staff_login.route('/staff/profile/update', methods=['POST'])
def staff_profile_update():
    if 'loggedin' in session and session['role'] in ('staff', 'manager', 'admin'):
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']

        sql = "UPDATE staff SET firstname = %s, lastname = %s, phone = %s where accountid = %s;"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, (firstName, lastName, phone, session['accountid']))
        mysql.connection.commit()
        flash("Profile updated", "success")
        if session['role'] == 'staff':
            return redirect(url_for('staff_login.staff_profile'))
        elif session['role'] == 'manager':
            return redirect(url_for('staff_login.manager_profile'))
        elif session['role'] == 'admin':
            return redirect(url_for('staff_login.admin_profile'))
        else:
            return redirect(url_for('staff_login.stafflogin'))
    
    flash("Please log in ", "warning")
    return redirect(url_for('staff_login.stafflogin'))