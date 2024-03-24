from app import mysql
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
import re
import bcrypt,secrets,string

manage_staff = Blueprint('manage_staff', __name__)

@manage_staff.route('/manage/staff', methods=['POST', 'GET'])
def manage_employees():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = """
                SELECT s.*,r.* FROM staff s
                LEFT JOIN accounts a ON s.accountid=a.accountid
                LEFT JOIN roles r ON a.roleid=r.roleid
                WHERE a.roleid = 3;
                """
            
            cursor.execute(sql)
            employee_information = cursor.fetchall()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = """
                SELECT * FROM roles WHERE role <> 'customer'; 
                        """
            cursor.execute(sql)
            roles = cursor.fetchall()
            return render_template('manage_staff.html', employee_informations=employee_information,roles=roles)
        else:
            #Get data from javascript submit form
            selected_switch_value = request.form.get('statusValue')
            staffid=request.form.get('staffId')
 
            #update the database when user change status
            if selected_switch_value == 'Active':  
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE staff SET is_active = '0' WHERE staffid = %s;",(staffid,))
                mysql.connection.commit()
                selected_switch_value="Inactive"
            elif selected_switch_value == 'Inactive':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE staff SET is_active = '1' WHERE staffid = %s;",(staffid,))
                mysql.connection.commit()
                selected_switch_value="Active"
            #Ticket Check ID is also bsid 
            flash("Update Staff ID #{} status to '{}' ".format(staffid, selected_switch_value), 'success')  
            return redirect(url_for('manage_staff.manage_employees',staffid=staffid))    
    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@manage_staff.route('/edit/staff', methods=['POST', 'GET'])
def staff_edit():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        staffid = request.args.get("staffid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            select s.*, DATE_FORMAT(s.join_date,'%%d/%%m/%%Y') AS jd
            from staff s
            where staffid = %s
        """
        cursor.execute(sql, (staffid, ))
        employee_informations = cursor.fetchall()

        return render_template("staff_edit.html", employee_informations=employee_informations)
    else:
   
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
        

@manage_staff.route('/role_change/staff', methods=['POST'])
def staff_role_change():
    if 'loggedin' in session and session['role'] == 'admin':
        accountid = request.form.get("accountid")
        staffid= request.form.get("staffid")
        new_roleid = request.form.get("roleid")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                SELECT * FROM roles WHERE roleid = %s;
                        """
        cursor.execute(sql,(new_roleid, ))
        role = cursor.fetchone()
        new_role=role['role']
        print("new_role",new_role)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete staff with that accountid
        cursor.execute("UPDATE accounts SET roleid = %s WHERE accountid = %s;", (new_roleid,accountid,))
        mysql.connection.commit()
        flash(f"Staff ID #{staffid}'s role has now been changed to '{new_role}' ", "success")
        return redirect(url_for('manage_staff.manage_employees'))
    else:
        flash("Plase login as manager or admin to change roles", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@manage_staff.route('/add/staff')
def staff_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
         # Define a character set containing letters and digits
        alphabet = string.ascii_letters + string.digits

        # Define a password length, for example, 12 characters
        length = 12

        # Use secrets.choice function and join method to generate a random string as a temporary password
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        temporary_password = password
        return render_template('staff_add.html',temporary_password=temporary_password)
    else:
        flash("Plase login as manager or admin to add new staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
    
@manage_staff.route('/add_db/staff', methods=['POST', 'GET'])
def staff_add_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'POST':
            add_email = request.form['email'].strip()
            email = add_email + '@moviemagic.com'
            phone = request.form['phone'].strip()
            firstname = request.form['firstname'].strip()
            lastname = request.form['lastname'].strip()
            password = request.form['tem_pwd']
            roleid = '3'
            join_date = request.form['join_date']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Insert user data into the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            # Hashing the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
            cursor.execute('INSERT INTO accounts (username, password, roleid) VALUES (%s, %s, %s)',
                                    (email, hashed_password, roleid))
            mysql.connection.commit()
            new_account_id = cursor.lastrowid
            cursor.execute('INSERT INTO staff (firstname, lastname, email, phone, accountid,join_date) VALUES (%s, %s, %s, %s, %s, %s)',
                                (firstname, lastname, email, phone, new_account_id,join_date))
            mysql.connection.commit()
            new_staff_id = cursor.lastrowid
            
            flash("New Staff #ID {} added successfully!".format(new_staff_id), "success")
            return redirect(url_for('manage_staff.manage_employees'))
        else:
            flash("Invalid request method. Please try again.", "error")    
            return redirect(url_for('manage_staff.manage_employees'))         
    else:
        flash("Plase login as admin or manager to add new staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
 
    
@manage_staff.route('/update/staff', methods=['POST', 'GET'])
def staff_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        staffid = request.form['staffid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']      

        parameters_staff = (firstname, lastname, email, phone, staffid)
        sql_staff = """
                UPDATE staff
                SET firstname = %s, lastname = %s, email = %s, phone = %s
                WHERE staffid = %s;
            """
        # update staff table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_staff, parameters_staff)
        mysql.connection.commit()
        flash(f"Staff - id {staffid} - {firstname}{lastname} is now updated", "success")
        return redirect(url_for('manage_staff.manage_employees'))
    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
