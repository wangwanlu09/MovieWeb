from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone
import re

manage_settings = Blueprint('manage_settings', __name__)

@manage_settings.route('/settings/contact')
def setting_contactinfo():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from company where latest_version = 1;")
        company = cursor.fetchone()
        return render_template('setting_company.html', company = company)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin'))
    
@manage_settings.route('/settings/contact/update', methods=['POST'])
def contact_update():
    if 'loggedin' in session and session['role'] =='admin'and request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']
        street = request.form['street']
        city = request.form['city']
        country = request.form['country']
        postcode = request.form['postcode']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address", "warning")
            return redirect(url_for('manage_settings.setting_contactinfo'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # deactivate previous records
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')
        sql_deactivate = """
                UPDATE company
                SET latest_version = 0, updated_date = %s 
                WHERE latest_version = 1
            """
        cursor.execute(sql_deactivate, (today, ))

        # update the latest version
        sql_update = """
            INSERT INTO company (phone, email, street, city, country, postcode, created_date, updated_date)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        parameters = (phone, email, street, city, country, postcode, today, today)
        cursor.execute(sql_update, parameters)

        # commit changes
        mysql.connection.commit()
        flash("Contact information is now updated", "success")
        return redirect(url_for('staff_login.admindashboard'))  
    else:
        flash("Only admin can edit settings")
        return redirect(url_for('staff_login.stafflogin'))    
    
@manage_settings.route('/settings/genre')
def setting_genre():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from genre;")
        genre = cursor.fetchall()
        return render_template('setting_genre.html', genre = genre)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin'))    

@manage_settings.route('/settings/genre/add', methods=['POST'])
def setting_genre_add():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        genre = request.form['genre']
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """INSERT INTO genre (genre_name, created_date, updated_date) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (genre, today, today))
        # commit changes
        mysql.connection.commit()
        flash(f"New genre {genre} is now added.", "success")
        return redirect(url_for('manage_settings.setting_genre'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/genre/edit')
def setting_genre_edit():
    if 'loggedin' in session and session['role'] =='admin':
        genreid = request.args.get('genreid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from genre where genreid = %s;", (genreid, ))
        genre = cursor.fetchone()
        return render_template('setting_genre_edit.html', genre = genre)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/genre/update', methods=['POST'])
def setting_genre_update():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        genre_name = request.form['genre']
        genreid =  request.form['genreid']
        
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE genre SET genre_name = %s, updated_date = %s WHERE genreid = %s;", (genre_name, today, genreid))
        # commit changes
        mysql.connection.commit()

        flash(f"Genre id #{genreid} is now updated.", "success")
        return redirect(url_for('manage_settings.setting_genre'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/genre/delete')
def setting_genre_delete():
    if 'loggedin' in session and session['role'] =='admin':
        genreid = request.args.get('genreid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM genre where genreid = %s;", (genreid, ))
        # commit changes
        mysql.connection.commit()
        flash(f"Genre id #{genreid} is now deleted.", "success")
        return redirect(url_for('manage_settings.setting_genre'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/actors')
def setting_actors():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from actors;")
        actors = cursor.fetchall()
        return render_template('setting_actors.html', actors = actors)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin'))  

@manage_settings.route('/settings/actors/add', methods=['POST'])
def setting_actor_add():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        actor_name = firstname + ' ' + lastname
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """INSERT INTO actors (actor_name, firstname, lastname, created_date, updated_date) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (actor_name, firstname, lastname, today, today))
        # commit changes
        mysql.connection.commit()
        flash(f"New genre {actor_name} is now added.", "success")
        return redirect(url_for('manage_settings.setting_actors'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 


@manage_settings.route('/settings/actors/edit')
def setting_actor_edit():
    if 'loggedin' in session and session['role'] =='admin':
        actorid = request.args.get('actorid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from actors where actorid = %s;", (actorid, ))
        actor = cursor.fetchone()
        return render_template('setting_actor_edit.html', actor = actor)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin'))   

@manage_settings.route('/settings/actor/update', methods=['POST'])
def setting_actor_update():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        actorid = request.form['actorid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        actor_name = firstname + ' ' + lastname
        
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "UPDATE actors SET actor_name = %s, firstname = %s, lastname = %s, updated_date = %s WHERE actorid = %s;"
        parameters = (actor_name, firstname, lastname, today, actorid)
        cursor.execute(sql, parameters)
        # commit changes
        mysql.connection.commit()

        flash(f"Actor id #{actorid} is now updated.", "success")
        return redirect(url_for('manage_settings.setting_actors'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/actor/delete')
def setting_actor_delete():
    if 'loggedin' in session and session['role'] =='admin':
        actorid = request.args.get('actorid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM actors where actorid = %s;", (actorid, ))
        # commit changes
        mysql.connection.commit()
        flash(f"Actor id #{actorid} is now deleted.", "success")
        return redirect(url_for('manage_settings.setting_actors'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/ratings')
def setting_ratings():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from ratings;")
        ratings = cursor.fetchall()
        return render_template('setting_ratings.html', ratings = ratings)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin'))    

@manage_settings.route('/settings/rating/add', methods=['POST'])
def setting_rating_add():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        rating = request.form['rating']
        color = request.form['color']
        desc = request.form['desc']
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """INSERT INTO ratings (rating_code, color, created_date, updated_date, descriptions) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (rating, color, today, today, desc))
        # commit changes
        mysql.connection.commit()
        flash(f"New rating {rating} is now added.", "success")
        return redirect(url_for('manage_settings.setting_ratings'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/rating/edit')
def setting_rating_edit():
    if 'loggedin' in session and session['role'] =='admin':
        ratingid = request.args.get('ratingid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from ratings where ratingid = %s;", (ratingid, ))
        rating = cursor.fetchone()
        colorlist = ["yellow", "green", "red", "purple"]
        return render_template('setting_rating_edit.html', rating = rating, colorlist = colorlist)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/rating/update', methods=['POST'])
def setting_rating_update():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        ratingid = request.form['ratingid']
        ratingcd = request.form['ratingcd']
        color =  request.form['color']
        desc = request.form['desc']
        
        now = datetime.now(timezone('Pacific/Auckland'))
        today = now.strftime('%Y-%m-%d')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE ratings SET rating_code = %s, color = %s, updated_date = %s, descriptions = %s WHERE ratingid = %s;", (ratingcd, color, today, desc, ratingid))
        # commit changes
        mysql.connection.commit()

        flash(f"Rating id #{ratingid} is now updated.", "success")
        return redirect(url_for('manage_settings.setting_ratings'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/rating/delete')
def setting_rating_delete():
    if 'loggedin' in session and session['role'] =='admin':
        ratingid = request.args.get('ratingid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM ratings where ratingid = %s;", (ratingid, ))
        # commit changes
        mysql.connection.commit()
        flash(f"Rating id #{ratingid} is now deleted.", "success")
        return redirect(url_for('manage_settings.setting_ratings'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/admin/messages')
def view_messages():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from contact_message order by send_datetime DESC")
        messages = cursor.fetchall()
        return render_template("contact_messages.html", messages=messages)
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 
    

@manage_settings.route('/admin/cinema_names')
def setting_cinema_names():
    if 'loggedin' in session and session['role'] =='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from cinemas order by cinemaid ASC")
        cinemas = cursor.fetchall()
        return render_template("setting_cinema_names.html", cinemas=cinemas)        

@manage_settings.route('/settings/cinema_names/add', methods=['POST'])
def setting_cinema_names_add():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        cinema_name = request.form['cinema_name'].strip()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """INSERT INTO cinemas (name) VALUES (%s)"""
        cursor.execute(sql, (cinema_name,))
        # commit changes
        mysql.connection.commit()
        flash(f"New cinema {cinema_name} is now added.", "success")
        return redirect(url_for('manage_settings.setting_cinema_names'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/cinema_name/edit')
def setting_cinema_name_edit():
    if 'loggedin' in session and session['role'] =='admin':
        cinemaid = request.args.get("cinemaid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from cinemas where cinemaid = %s;", (cinemaid, ))
        cinema = cursor.fetchone()
        return render_template('setting_cinema_name_edit.html', cinema = cinema)
    else:
        flash("Only admin can edit cinema names", "warning")
        return redirect(url_for('staff_login.stafflogin')) 

@manage_settings.route('/settings/cinema_name/update', methods=['POST'])
def setting_cinema_name_update():
    if 'loggedin' in session and session['role'] =='admin' and request.method == 'POST':
        cinemaid = request.form['cinemaid']
        cinema_name = request.form['cinema_name']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE cinemas SET name = %s WHERE cinemaid = %s;", (cinema_name, cinemaid))
        # commit changes
        mysql.connection.commit()

        flash(f"Cinema id #{cinemaid} is now updated.", "success")
        return redirect(url_for('manage_settings.setting_cinema_names'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 
    
@manage_settings.route('/settings/cinema_name/delete')
def setting_cinema_name_delete():
    if 'loggedin' in session and session['role'] =='admin':
        cinemaid = request.args.get("cinemaid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM cinemas where cinemaid = %s;", (cinemaid, ))
        # commit changes
        mysql.connection.commit()
        flash(f"Cinema id #{cinemaid} is now deleted.", "success")
        return redirect(url_for('manage_settings.setting_cinema_names'))
    else:
        flash("Only admin can edit settings", "warning")
        return redirect(url_for('staff_login.stafflogin')) 