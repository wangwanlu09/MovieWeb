from app import mysql
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, url_for, redirect, session, request, flash, make_response, jsonify
import MySQLdb.cursors
import re,random
import bcrypt

manage_customers = Blueprint('manage_customers', __name__)

@manage_customers.route('/manage/customers', methods=['POST', 'GET'])
def manage_customer():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        if request.method == 'GET':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = """
                SELECT *
                FROM
                    customers;
            """
            
            cursor.execute(sql)
            customers_information = cursor.fetchall()

            return render_template('manage_customers.html', customers_informations=customers_information)
        else:
            #Get data from javascript submit form
            selected_switch_value = request.form.get('statusValue')
            customerid=request.form.get('customerId')
 
            #update the database when user change status
            if selected_switch_value == 'Active':  
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE customers SET is_active = '0' WHERE customerid = %s;",(customerid,))
                mysql.connection.commit()
                selected_switch_value="Inactive"
            elif selected_switch_value == 'Inactive':
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
                cursor.execute("UPDATE customers SET is_active = '1' WHERE customerid = %s;",(customerid,))
                mysql.connection.commit()
                selected_switch_value="Active"
            #Ticket Check ID is also bsid 
            flash("Update Customer ID #{} status to '{}' ".format(customerid, selected_switch_value), 'success')  
            return redirect(url_for('manage_customers.manage_customer',customerid=customerid))    

    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
        
@manage_customers.route('/edit/customers', methods=['POST', 'GET'])
def customers_edit():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        customerid = request.args.get("customerid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
            select c.* 
            from customers c
            where c.customerid = %s
        """
        cursor.execute(sql, (customerid, ))
        customers_information = cursor.fetchall()
        return render_template("customers_edit.html", customers_informations=customers_information)
    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
    
@manage_customers.route('/delete/customers', methods=['POST', 'GET'])
def cutomers_delete():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        customerid = request.args.get("customerid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # delete the account in account table, automatically delete customers with that accountid
        cursor.execute("DELETE a FROM accounts a LEFT JOIN customers c on a.accountid = c.accountid WHERE customerid = %s;", (customerid,))
        mysql.connection.commit()
        flash(f"customerid - {customerid} is now deleted", "success")
        return redirect(url_for('manage_customers.manage_customer'))
    else:
        flash("Plase login as manager or admin to delete staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@manage_customers.route('/add/customers')
def customers_add():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        return render_template('customers_add.html')
    else:
        flash("Plase login as manager or admin to add new staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
    
@manage_customers.route('/add_db/customers', methods=['POST', 'GET'])
def customers_add_db():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
            if request.method == 'POST':
                email = request.form['email'].strip()
                phone = request.form['phone'].strip()
                firstname = request.form['firstname'].strip()
                lastname = request.form['lastname'].strip()
                password = '88888888'
                roleid = '4'

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                try:
                    # Check if the email already exists
                    cursor.execute('SELECT * FROM accounts WHERE LOWER(username) = LOWER(%s)', (email,))
                    user = cursor.fetchone()

                    if user:
                        flash("Email address already registered!", "warning")

                    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        flash("Invalid email address!", "warning")

                    elif not re.match(r'^\d{11}$', phone):
                        flash("Phone number must be 11 digits!", "warning")

                    else:
                        # Insert user data into the database
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO accounts (username, password, roleid) VALUES (%s, %s, %s)',
                                                (email, hashed_password, roleid))
                        mysql.connection.commit()
                        new_account_id = cursor.lastrowid

                        cursor.execute('INSERT INTO customers (firstname, lastname, email, phone, accountid) VALUES (%s, %s, %s, %s, %s)',
                                                (firstname, lastname, email, phone, new_account_id,))
                        mysql.connection.commit()

                        flash("Added successfully!", "success")
                        return redirect(url_for('manage_customers.manage_customer'))

                except Exception as e:
                    # Handle exceptions (e.g., database errors)
                    print(f"Error: {e}")
                    flash("An error occurred. Please try again later.", "warning")

                finally:
                    cursor.close()

            return render_template('customers_add.html')


    else:
        flash("Plase login as manager or admin to add new staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))

    
@manage_customers.route('/update/customers', methods=['POST', 'GET'])
def customers_update():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        customerid = request.form['customerid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']      

        parameters_customers = (firstname, lastname, email, phone, customerid)
        sql_staff = """
                UPDATE customers
                SET firstname = %s, lastname = %s, email = %s, phone = %s
                WHERE customerid = %s;
            """
        # update staff table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql_staff, parameters_customers)
        mysql.connection.commit()
        flash(f"customer - id {customerid} - {firstname}{lastname} is now updated", "success")
        return redirect(url_for('manage_customers.manage_customer'))
    else:
        flash("Plase login as manager or admin to edit staff", "warning")
        return redirect(url_for('staff_login.stafflogin'))