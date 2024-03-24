import pandas
import bcrypt
import sys
sys.path.insert(0,'..')
import connect
import mysql.connector
import datetime


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.user, \
    password=connect.dbpw, host=connect.host, \
    database=connect.db, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# insert data to database
def insert(sql, parameters):
    connection = getCursor()
    connection.execute(sql, parameters)
    return connection.lastrowid

# accounts data
accounts = pandas.read_csv('data_accounts.csv')
# print(accounts)
for index, row in accounts.iterrows():
    sql = """
        INSERT INTO accounts (accountid, username, password, roleid)
        VALUES
        (%s, %s, %s, %s)
    """
    hashed_pw = bcrypt.hashpw(row['password'].encode('utf-8'), bcrypt.gensalt())
    parameters = (row['accountid'], row['username'], hashed_pw, row['roleid'])
    # print(row['accountid'], row['username'], row['password'], row['role'], hashed_pw)
    insert(sql, parameters)

# staff data
staff = pandas.read_csv('data_staff.csv', converters={'phone': str})
for index, row in staff.iterrows():
    sql = """
        INSERT INTO staff (staffid, firstname, lastname, email, phone, accountid, join_date)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    join_date = datetime.datetime.strptime(row['join_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['staffid'], row['firstname'], row['lastname'], row['email'], row['phone'], row['accountid'], join_date)
    insert(sql, parameters)
    

# customer data
customer = pandas.read_csv('data_customers.csv', converters={'phone': str})
for index, row in customer.iterrows():
    sql = """
        INSERT INTO customers (customerid, firstname, lastname, email, phone, accountid, join_date)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    join_date = datetime.datetime.strptime(row['join_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['customerid'], row['firstname'], row['lastname'], row['email'], row['phone'], row['accountid'], join_date)
    insert(sql, parameters)

# movie data
movies = pandas.read_csv('data_movies.csv')
for index, row in movies.iterrows():
    sql = """
        INSERT INTO movies (movieid, title, release_date, start_date,  descriptions, runtime_hour, runtime_minute, genreid, ratingid, image_url)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    release_date = datetime.datetime.strptime(row['release_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    start_date = datetime.datetime.strptime(row['start_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['movieid'], row['title'].strip('"'), release_date, start_date, row['descriptions'].strip('"'), row['runtime_hour'], row['runtime_minute'], row['genreid'], row['ratingid'], row['image_url'])
    insert(sql, parameters)

# actor data
actors = pandas.read_csv('data_actors.csv')
for index, row in actors.iterrows():
    sql = """
        INSERT INTO actors (actorid, actor_name, firstname, lastname, created_date, updated_date)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """
    created_date = datetime.datetime.strptime(row['created_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    updated_date = datetime.datetime.strptime(row['updated_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['actorid'], row['actor_name'], row['firstname'], row['lastname'], created_date, updated_date)
    insert(sql, parameters)

# bridging table for actors and movies
starring = pandas.read_csv('data_starring.csv')
for index, row in starring.iterrows():
    sql = """
        INSERT INTO starring (starringid, movieid, actorid)
        VALUES
        (%s, %s, %s)
        """
    starringid = row['starringid'].astype(str)
    movieid = row['movieid'].astype(str)
    actorid = row['actorid'].astype(str)
    parameters = (starringid, movieid, actorid)
    insert(sql, parameters)

# sessiontime tables - restrict session time for each cinema
sessiontime = pandas.read_csv('data_sessiontime.csv')
for index, row in sessiontime.iterrows():
    sql = """
        INSERT INTO sessiontime (sessiontime_id, sessiontime, maximum_time, cinemaid)
        VALUES 
        (%s, %s, %s, %s)
        """
    parameters = (row['sessiontime_id'], row['sessiontime'], row['maximum_time'], row['cinemaid'])
    insert(sql, parameters)
    
# movie schedules
schedules = pandas.read_csv('data_sessions.csv')
for index, row in schedules.iterrows():
    sql = """
        INSERT INTO sessions (sessionid, session_date, sessiontime_id, movieid)
        VALUES
        (%s, %s, %s, %s)
        """
    sessiondate = datetime.datetime.strptime(row['session_date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['sessionid'], sessiondate, row['sessiontime_id'], row['movieid'])
    insert(sql, parameters)

dates = pandas.read_csv('data_dates.csv')
for index, row in dates.iterrows():
    sql = """
        INSERT INTO dates (dateid, date, weekday_number, weekday_name)
        VALUES
        (%s, %s, %s, %s)
        """
    date = datetime.datetime.strptime(row['date'], "%d/%m/%Y").strftime("%Y-%m-%d")
    parameters = (row['dateid'], date, row['weekday_number'], row['weekday_name'])
    insert(sql, parameters)

seats = pandas.read_csv('data_seats.csv')
for index, row in seats.iterrows():
    sql = """
        INSERT INTO seats (seatid, seat_number, cinemaid)
        VALUES
        (%s, %s, %s)
        """
    parameters = (row['seatid'], row['seat_number'], row['cinemaid'])
    insert(sql, parameters)

# promotions = pandas.read_csv('data_promotions.csv')
# for index, row in promotions.iterrows():
#     sql = """
#         INSERT INTO promotions (promotionid, promotion_code, effective_date, expiration_date, promotion_type, title, descriptions, details, image)
#         VALUES
#         (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#     effective = row['effective_date'].strip('"')
#     expiration = row['expiration_date'].strip('"')
#     parameters = (row['promotionid'], row['promotion_code'].fillna(''), effective, expiration, row['promotion_type'], row['title'], row['descriptions'], row['details'].strip('"'), row['image'])
#     insert(sql, parameters)

