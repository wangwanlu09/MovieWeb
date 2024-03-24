
from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session
import MySQLdb.cursors

test = Blueprint('test', __name__)

@test.route('/staff')
def staff():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from staff;")
    stafflist = cursor.fetchall()
    return render_template('test.html', stafflist = stafflist)