from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
import bcrypt
import re
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from datetime import date, datetime, timedelta
from pytz import timezone


registration = Blueprint('registration', __name__)

policy = PasswordPolicy.from_names(
    length=8,      # minimum length: 8 characters
    uppercase=1,   # require at least 1 uppercase letter
    numbers=1,     # require at least 1 digit
    strength= 0.2,   # require at least 0.2 with its entropy bits
)

@registration.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        username_email = request.form['username'] 
        username_email2 = request.form['confirm_username'] 
        firstname = request.form['firstname'] 
        lastname = request.form['lastname'] 
        phone = request.form['phone'] 
        password1 = request.form['password1'] 
        password2 = request.form['password2'] 
        roleid = 4 # customer
        stats = PasswordStats(password1)
        checkpolicy = policy.test(password1)


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Check if the email already exists
            cursor.execute('SELECT * FROM accounts WHERE LOWER(username) = LOWER(%s)', (username_email,))
            account = cursor.fetchone()

            if account:
                flash("Username already exists!", "warning")
                return redirect(url_for('registration.register'))    
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', username_email):
                flash("Invalid email address!", "warning")
                return redirect(url_for('registration.register'))
            else:
                if username_email != username_email2:
                    flash("Emails do not match. Please try again.", "warning")

                elif password1 != password2:
                    flash("Passwords do not match. Please try again", "warning")

                else:
                    if checkpolicy and stats.strength() < 0.3:
                        flash("Password not strong enough. Avoid consecutive characters and easily guessed words.","warning")
                        return redirect(url_for('registration.register'))
                    else:
                        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO accounts (username, password, roleid) VALUES (%s, %s, %s)',
                                        (username_email, hashed_password, roleid,))
                        new_account_id = cursor.lastrowid
                        now = datetime.now(timezone('Pacific/Auckland'))
                        localdate = now.strftime("%Y-%m-%d")
                        cursor.execute('INSERT INTO customers (firstname, lastname, email, phone, accountid, join_date) VALUES (%s, %s, %s, %s, %s, %s)',
                                        (firstname, lastname, username_email, phone, new_account_id, localdate))
                        # commit changes if both are successful
                        mysql.connection.commit()
                    
                        flash("You have successfully registered!", "success")
                        return redirect(url_for('registration.register'))
        except Exception as e:
        # Handle exceptions (e.g., database errors)
            print(f"Error: {e}")
            flash("An error occurred. Please try again later.", "warning")
        finally:
            cursor.close()
            return redirect(url_for('registration.register'))

    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username FROM accounts;')
        username = cursor.fetchall()
        usernames=[un for un in username if un is not None]

        return render_template('Register.html',usernames=usernames)

    

