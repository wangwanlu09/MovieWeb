from flask import Flask
from flask_mysqldb import MySQL
from app import connect

# def create_app():
app = Flask(__name__)
app.config['SECRET_KEY'] = 'moviemagicsecretkey'

app.config['MYSQL_HOST'] = connect.host
app.config['MYSQL_USER'] = connect.user
app.config['MYSQL_PASSWORD'] = connect.dbpw
app.config['MYSQL_DB'] = connect.db
app.config['MYSQL_PORT'] = connect.port

# Intialize MySQL
mysql = MySQL(app)

from app.stafflogin.views import staff_login
from app.customerlogin.views import customer_login
from app.home.views import home
from app.register.views import registration

from app.manage_movies.views import managemovies
from app.detailed.views import detailed
from app.manage_promotions.views import promotions
from app.manage_staff.views import manage_staff
from app.movieschedule.views import movie_schedule
from app.bookings.views import booking
from app.payment.views import payments
from app.manage_price.views import ticket_price
from app.giftcards.views import giftcards
from app.search_result.views import search_result
from app.coming_soon.views import coming_soon

from app.manage_settings.views import manage_settings
from app.check_in.views import checkIn
from app.manage_customers.views import manage_customers 
from app.manage_managers.views import manageManagers
from app.reports.views import reports

app.register_blueprint(staff_login)
app.register_blueprint(customer_login)
app.register_blueprint(home)
app.register_blueprint(registration)

app.register_blueprint(managemovies)
app.register_blueprint(detailed)
app.register_blueprint(manage_staff)
app.register_blueprint(promotions)
app.register_blueprint(movie_schedule)
app.register_blueprint(booking)
app.register_blueprint(payments)
app.register_blueprint(ticket_price)
app.register_blueprint(giftcards)
app.register_blueprint(search_result)
app.register_blueprint(coming_soon)

app.register_blueprint(manage_settings)
app.register_blueprint(checkIn)
app.register_blueprint(manage_customers)
app.register_blueprint(manageManagers)

app.register_blueprint(reports)


