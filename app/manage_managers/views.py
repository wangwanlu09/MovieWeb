from app import mysql
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, make_response, jsonify
import MySQLdb.cursors
import re,random
import bcrypt,secrets,string

manageManagers = Blueprint('manageManagers', __name__)

@manageManagers.route('/manage/manager', methods=['POST', 'GET'])
def manage_manager():
    if session['role']  == "admin":
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = """
                SELECT s.*,r.* FROM staff s
                LEFT JOIN accounts a ON s.accountid=a.accountid
                LEFT JOIN roles r ON a.roleid=r.roleid
                where a.roleid = 2
                """
            
            cursor.execute(sql)
            managerInfo = cursor.fetchall()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = "SELECT * FROM roles WHERE roleid <> 4;"
            cursor.execute(sql)
            roles = cursor.fetchall()
            return render_template('manage_managers.html', managerInfo=managerInfo,roles=roles)
        else:
            #Get data from javascript submit form
            selected_switch_value = request.form.get('statusValue')
            staffid=request.form.get('staffid')
 
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
            return redirect(url_for('manageManagers.manage_manager',staffid=staffid))    

    else:
        flash("Plase login as admin to edit managers", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@manageManagers.route('/role_change/manager', methods=['POST'])
def manager_role_change():
    if 'loggedin' in session and session['role'] == 'admin':

        # 
        accountid = request.form.get("accountid")
        staffid= request.form.get("staffid")
        new_roleid = request.form.get("roleid")
   
        #provide role options for user to select
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                SELECT * FROM roles WHERE roleid = %s;
                        """
        cursor.execute(sql,(new_roleid, ))
        role = cursor.fetchone()
        new_role=role['role']
      
        #update manager's role to new role in database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET roleid = %s WHERE accountid = %s;", (new_roleid,accountid,))
        mysql.connection.commit()
        flash(f"Manager ID #{staffid}'s role has now been changed to '{new_role}' ", "success")
        return redirect(url_for('manageManagers.manage_manager'))
    else:
        flash("Plase login as manager or admin to change roles", "warning")
        return redirect(url_for('staff_login.stafflogin'))


@manageManagers.route('/edit/managers', methods=['POST', 'GET'])
def edit_manager():
    if session['role']  == "admin":
        staffid = request.args.get("staffid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            select s.*, DATE_FORMAT(s.join_date,'%%d/%%m/%%Y') AS jd
            from staff s
            where staffid = %s
        """
        cursor.execute(sql, (staffid, ))
        manager_info = cursor.fetchall()
        return render_template("manage_manager_edit.html", manager_info=manager_info)
    else:
        flash("Plase login as admin to edit managers", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
    
# @manageManagers.route('/delete/manager', methods=['POST', 'GET'])
# def delete_manager():
#     if session['role']  == "admin":
#         managerid = request.args.get("managerid")
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         # delete the account in account table, automatically delete customers with that accountid
#         cursor.execute("DELETE a FROM accounts a LEFT JOIN managers m on a.accountid = m.accountid WHERE managerid = %s;", (managerid,))
#         mysql.connection.commit()
#         flash(f"Managerid #{managerid} is now deleted", "success")
#         return redirect(url_for('manageManagers.manage_manager'))
#     else:
#         flash("Plase login as admin to delete managers", "warning")
#         return redirect(url_for('staff_login.stafflogin'))

@manageManagers.route('/add/manager',methods=['GET','POST'])
def add_manager():
    if session['role']  == "admin":

        # Define a character set containing letters and digits
        alphabet = string.ascii_letters + string.digits

        # Define a password length, for example, 12 characters
        length = 12

        # Use secrets.choice function and join method to generate a random string as a temporary password
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        temporary_password = password
        return render_template('manage_manager_add.html',temporary_password=temporary_password)
        
    else:
        flash("Plase login admin to add new staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    

@manageManagers.route('/add_db/manager', methods=['POST', 'GET'])
def add_manager_db():
    if session['role']  == "admin":
        if request.method == 'POST':
            # Extracting and processing form data
            email_prefix = request.form['email'].strip()
            email= email_prefix + '@moviemagic.com'
            phone = request.form['phone'].strip()
            firstname = request.form['firstname'].strip()
            lastname = request.form['lastname'].strip()
            password = request.form['tem_pwd']
            roleid = '2' 

            join_date = request.form['join_date']
            
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
            
            flash("New Manager #ID {} added successfully!".format(new_staff_id), "success")
            return redirect(url_for('manageManagers.manage_manager'))
        else:
            flash("Invalid request method. Please try again.", "error")    
            return redirect(url_for('manageManagers.manage_manager'))         
    else:
        flash("Plase login admin to add new managers", "warning")
        return redirect(url_for('staff_login.stafflogin'))

    
@manageManagers.route('/update/manager', methods=['POST', 'GET'])
def update_manager():
    if session['role']  == "admin":
        # Extracting and processing form data
        staffid = request.form['staffid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']      

        parameters_customers = (firstname, lastname, email, phone, staffid)
        sql_staff = """
                UPDATE staff
                SET firstname = %s, lastname = %s, email = %s, phone = %s
                WHERE staffid = %s;
            """
        # update staff table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_staff, parameters_customers)
        mysql.connection.commit()
        flash(f"Staff ID #{staffid} - {firstname}{lastname} is now updated", "success")
        return redirect(url_for('manageManagers.manage_manager'))
    else:
        flash("Plase login as admin to edit manager", "warning")
        return redirect(url_for('staff_login.stafflogin'))
