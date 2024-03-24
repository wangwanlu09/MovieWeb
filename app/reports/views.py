from app import mysql
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
import MySQLdb.cursors
from datetime import date, datetime, timedelta
from pytz import timezone

reports = Blueprint('reports', __name__)
@reports.route('/reports/overview')
def report_overview():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
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

        # ticket salse scheduled
        cursor.execute("select COALESCE(SUM(no_of_tickets),0) as ticketsales_num from booking_transactions where transaction_date between %s and %s", parameters_date)
        ticketsales_num = cursor.fetchone()['ticketsales_num']

        # giftcard sales
        cursor.execute("select COALESCE(SUM(amount),0) as giftcard_num from payment where payment_type = 'giftcard' and payment_date between %s and %s", parameters_date)
        giftcard_num = cursor.fetchone()['giftcard_num']

        # top 5 movies
        sql = """
        with cte as (
            select m.title, COALESCE(SUM(bt.no_of_tickets),0) as ticketnum
            from bookings b
            left join booking_transactions bt on b.bookingid = bt.bookingid
            left join sessions s on s.sessionid = b.sessionid
            left join movies m on m.movieid = s.movieid
            where booking_date between %s and %s
            group by m.title
            order by COALESCE(SUM(bt.no_of_tickets),0) DESC
            limit 5
            )
            select title, cast(ticketnum as SIGNED) as ticketnum
            from cte
            """
        cursor.execute(sql, parameters_date)
        top5Movies = cursor.fetchall()
        top5Movies = sorted(top5Movies, key=lambda x: (x['ticketnum']), reverse = True ) 
        top5names = [ sub['title'] for sub in top5Movies ]
        top5values = [ sub['ticketnum'] for sub in top5Movies ]

        # sales trend
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            , cte_bookings as (
                select WEEK(booking_date, 1) as weeknum
                ,COALESCE(SUM(total_amount),0) as ticketamt
                ,COALESCE(SUM(payment_amount),0) as paymentamt
                from bookings 
                where booking_date between %s and %s
                group by WEEK(booking_date, 1)
            )
            select w.week_start,  cast(b.ticketamt as SIGNED) as ticketamt
            ,cast(b.paymentamt as SIGNED) as paymentamt
            from cte_bookings b
            left join cte_wkstart w on w.weeknum = b.weeknum
            order by w.week_start
            """
        cursor.execute(sql, parameters_date)
        sales = cursor.fetchall()
        salesWeek = [ sub['week_start'].strftime('%d/%m/%Y') for sub in sales ]
        salesValue = [ sub['ticketamt'] for sub in sales ]
        paymentamt = [ sub['paymentamt'] for sub in sales ]

        # giftcard sales
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            , cte_bookings as (
                select WEEK(transaction_date, 1) as weeknum
                ,COALESCE(SUM(no_of_tickets),0) as ticketnum
                from booking_transactions
                where transaction_date between %s and %s
                group by WEEK(transaction_date, 1)
            )
            select w.week_start,  cast(b.ticketnum as SIGNED) as ticketnum
            from cte_bookings b
            left join cte_wkstart w on w.weeknum = b.weeknum
            
            """
        cursor.execute(sql, parameters_date)
        ticketnums = cursor.fetchall()
        ticketcount = [ sub['ticketnum'] for sub in ticketnums ]
        return render_template("report_overview.html", newcustomers=newcustomers, countbookings=countbookings, ticketsales_amt=ticketsales_amt, ticketsales_num=ticketsales_num, giftcard_num=giftcard_num,\
                               top5names=top5names, top5values=top5values, salesWeek=salesWeek, salesValue=salesValue, paymentamt=paymentamt, ticketcount=ticketcount)
    else:
        flash("Please login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

@reports.route("/reports/sales")
def report_sales():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        today = datetime.now(timezone('Pacific/Auckland'))
        date30 = today + timedelta(days=-30)
        parameters_date = (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

        # sales per booking
        cursor.execute("select round(COALESCE(SUM(total_amount),0) / count(bookingid), 2) as salesbk from bookings where booking_date between %s and %s", parameters_date)
        salesbk = cursor.fetchone()['salesbk']

        # sales per ticket
        sql = """
            select round((select COALESCE(SUM(total_amount),0) as sales from bookings where booking_date between %s and %s) / 
            (select COALESCE(SUM(no_of_tickets),0) as ticketnum from booking_transactions where transaction_date between %s and %s), 2) 
            as salestk
            """
        cursor.execute(sql, (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
        salestk = cursor.fetchone()['salestk']

        # Top seller
        sql = """
            select m.title, COALESCE(SUM(b.total_amount),0) as salesmovie 
            from bookings b
            left join sessions s on s.sessionid = b.sessionid
            left join movies m on s.movieid = m.movieid
            where booking_date between %s and %s
            group by m.title
            order by COALESCE(SUM(b.total_amount),0) desc
            limit 1
            """
        cursor.execute(sql, parameters_date)
        salesmovie = cursor.fetchone()


        # ticket salse scheduled
        cursor.execute("select COALESCE(SUM(no_of_tickets),0) as ticketsales_num from booking_transactions where transaction_date between %s and %s", parameters_date)
        ticketsales_num = cursor.fetchone()['ticketsales_num']

        # giftcard sales
        sql = """
            with cte_gcpayment as (
                select g.giftcard_type_id, count(g.giftcardid) as countgc
                from payment p
                inner join giftcard_payment gp on gp.paymentid = p.paymentid
                inner join giftcards g on g.giftcardid = gp.giftcardid
                where p.payment_type = 'giftcard'
                and payment_date between %s and %s
                group by g.giftcard_type_id
                order by count(g.giftcardid) desc
                limit 1
            )
            select gt.giftcard_name, g.countgc
            from cte_gcpayment g
            left join giftcard_types gt on g.giftcard_type_id = gt.giftcard_type_id
            """
        cursor.execute(sql, parameters_date)
        gcsales = cursor.fetchone()


        # sales trend
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            , cte_bookings as (
                select WEEK(booking_date, 1) as weeknum
                ,COALESCE(SUM(total_amount),0) as ticketamt
                from bookings 
                where booking_date between %s and %s
                group by WEEK(booking_date, 1)
            )
            select w.week_start,  cast(b.ticketamt as SIGNED) as ticketamt
            from cte_bookings b
            left join cte_wkstart w on w.weeknum = b.weeknum
            order by w.week_start
            """
        cursor.execute(sql, parameters_date)
        sales = cursor.fetchall()
        salesWeek = [ sub['week_start'].strftime('%d/%m/%Y') for sub in sales ]
        salesValue = [ sub['ticketamt'] for sub in sales ]

        # ticket type sales
        sql = """
            select ticket_type, count(no_of_tickets) as tkcount
            from booking_transactions bt
            left join tickets t on t.ticketid = bt.ticketid
            where transaction_date between %s and %s
            group by ticket_type
            """
        cursor.execute(sql, parameters_date)
        tksales = cursor.fetchall()
        ticket_type = [ sub['ticket_type'] for sub in tksales ]
        tkcount = [ sub['tkcount'] for sub in tksales ]

        # giftcard sales
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            ,cte_gcpayment as (
                select week(p.payment_date, 1) as weeknum
                , count(gp.giftcardid) as gccount, COALESCE(sum(p.amount), 0) as gcamount
                from giftcard_payment gp
                left join payment p on p.paymentid = gp.paymentid
                where p.payment_type = 'giftcard'
                and payment_date between %s and %s
                group by week(p.payment_date, 1)
            )

            select w.week_start, g.gccount, cast(gcamount as signed) as gcamount
            from cte_gcpayment g 
            left join cte_wkstart w on w.weeknum = g.weeknum
            order by w.week_start
            """
        cursor.execute(sql, parameters_date)
        gctrend = cursor.fetchall()
        gcweek = [ sub['week_start'].strftime('%d/%m/%Y') for sub in gctrend ]
        gccount = [ sub['gccount'] for sub in gctrend ]
        gcamount = [ sub['gcamount'] for sub in gctrend ]


         # giftcard group
        sql = """
        with cte as (
            select gt.giftcard_name
            , COALESCE(SUM(g.giftcard_value), 0) as gcamt, count(g.giftcardid) as gcct
            from giftcards g
            left join giftcard_types gt on gt.giftcard_type_id = g.giftcard_type_id
            left join giftcard_payment gp on gp.giftcardid = g.giftcardid
            left join payment p on p.paymentid = gp.paymentid
            where payment_date between %s and %s
            group by gt.giftcard_name
            )
        select giftcard_name, cast(gcamt as signed) as gcamt, gcct from cte
        """
        cursor.execute(sql, parameters_date)
        gcgroup = cursor.fetchall()
        gctypes = [ sub['giftcard_name'] for sub in gcgroup ]
        gcct = [ sub['gcct'] for sub in gcgroup ]
        gcamt = [ sub['gcamt'] for sub in gcgroup ]

        # giftcard by value
        sql = """
                select concat('$', cast(g.giftcard_value as char(10)) ) as valuecat
                , count(g.giftcardid) as valuecount
                from giftcards g
                left join giftcard_payment gp on gp.giftcardid = g.giftcardid
                left join payment p on p.paymentid = gp.paymentid
                where p.payment_date between %s and %s
                group by g.giftcard_value
                order by count(g.giftcardid) desc
                limit 5
            """
        cursor.execute(sql, parameters_date)
        valuegroup = cursor.fetchall()
        valuecat = [ sub['valuecat'] for sub in valuegroup ]
        valuecount = [ sub['valuecount'] for sub in valuegroup ]

        # sales per customers
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            , cte_sales as (
                select week(booking_date, 1) as weeknum
                ,round(COALESCE(sum(total_amount),0) / count(distinct customerid)) as salespercus
                ,round(COALESCE(sum(total_amount),0) / count(bookingid), 2) as salesperbk
                from bookings 
                where booking_date between %s and %s
                group by week(booking_date, 1)
            )
            select w.week_start, salespercus, salesperbk
            from cte_sales s
            left join cte_wkstart w on w.weeknum = s.weeknum
            order by w.week_start
            """
        cursor.execute(sql, parameters_date)
        avgsales = cursor.fetchall()
        saleswk = [ sub['week_start'].strftime('%d/%m/%Y') for sub in avgsales ]
        salespercus = [ sub['salespercus'] for sub in avgsales ]
        salesperbk = [ sub['salesperbk'] for sub in avgsales ]


        return render_template("report_sales.html", salesbk=salesbk, salestk=salestk, salesmovie=salesmovie, ticketsales_num=ticketsales_num, gcsales=gcsales,\
                              salesWeek=salesWeek, salesValue=salesValue, ticket_type=ticket_type, tkcount=tkcount, gcweek=gcweek, gccount=gccount, gcamount=gcamount,\
                                gctypes=gctypes, gcct=gcct, gcamt=gcamt, valuecat=valuecat, valuecount=valuecount, saleswk=saleswk, salespercus=salespercus, salesperbk=salesperbk)
    else:
        flash("Please login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

    
@reports.route('/reports/customers')
def report_customers():
    if 'loggedin' in session and session['role'] in ('manager', 'admin'):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        today = datetime.now(timezone('Pacific/Auckland'))
        date30 = today + timedelta(days=-30)
        parameters_date = (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

        # new customer counts
        cursor.execute("select count(customerid) as newcustomers from customers where join_date between %s and %s", parameters_date)
        newcustomers = cursor.fetchone()['newcustomers']

        # tickets per customers
        cursor.execute("""select round(COALESCE(SUM(bt.no_of_tickets),0) / count(distinct b.customerid), 2) as ticektpercus from booking_transactions bt
            left join bookings b on b.bookingid = bt.bookingid where b.booking_date between %s and %s""", parameters_date)
        ticektpercus = cursor.fetchone()['ticektpercus']

        # sales per customers
        cursor.execute("""select round(COALESCE(SUM(total_amount),0) / count(distinct customerid), 2) as salespercus
            from bookings where booking_date between %s and %s""", parameters_date)
        salespercus = cursor.fetchone()['salespercus']

        # ticket salse scheduled
        cursor.execute("select COALESCE(SUM(no_of_tickets),0) as ticketsales_num from booking_transactions where transaction_date between %s and %s", parameters_date)
        ticketsales_num = cursor.fetchone()['ticketsales_num']

        # giftcard per customer
        sql = """
                select round(count(giftcardid) / count(distinct customerid), 2) as giftcard_num
                from giftcard_payment gp
                left join payment p on p.paymentid = gp.paymentid
                where p.payment_type = 'giftcard'
                and payment_date between %s and %s
            """
        cursor.execute(sql, parameters_date)
        giftcard_num = cursor.fetchone()['giftcard_num']

        # top 5 movies
        sql = """
        with cte as (
            select m.title, COALESCE(SUM(bt.no_of_tickets),0) as ticketnum
            from bookings b
            left join booking_transactions bt on b.bookingid = bt.bookingid
            left join sessions s on s.sessionid = b.sessionid
            left join movies m on m.movieid = s.movieid
            where booking_date between %s and %s
            group by m.title
            order by COALESCE(SUM(bt.no_of_tickets),0) DESC
            limit 5
            )
            select title, cast(ticketnum as SIGNED) as ticketnum
            from cte
            """
        cursor.execute(sql, parameters_date)
        top5Movies = cursor.fetchall()
        top5Movies = sorted(top5Movies, key=lambda x: (x['ticketnum']), reverse = True ) 
        top5names = [ sub['title'] for sub in top5Movies ]
        top5values = [ sub['ticketnum'] for sub in top5Movies ]

        # new customer trend
        sql = """
            with cte_wkstart as (
                select week(date, 1) as weeknum, min(date) as week_start
                from dates 
                group by week(date, 1)
            )
            , cte_customer as (
                select WEEK(join_date, 1) as weeknum
                ,count(distinct customerid) as newcustomer
                from customers 
                where join_date between %s and %s
                group by WEEK(join_date, 1)
            )
            ,cte_customer_tk as (
                select WEEK(b.booking_date, 1) as weeknum
                ,count(distinct c.customerid) as countbk
                from customers c
                left join bookings b on c.customerid = b.customerid
                where c.join_date between %s and %s
                and b.booking_date between %s and %s
                group by WEEK(b.booking_date, 1)
                having count(b.bookingid) >= 1
            )
            select w.week_start,  ifnull(c.newcustomer,0) as newcustomer, ifnull(b.countbk, 0) as countbk
            from cte_customer c
            inner join cte_wkstart w on w.weeknum = c.weeknum
            left join cte_customer_tk b on w.weeknum = b.weeknum
            order by w.week_start
            """
        cursor.execute(sql, (date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'), date30.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
        newcustomerstrend = cursor.fetchall()
        customerWeek = [ sub['week_start'].strftime('%d/%m/%Y') for sub in newcustomerstrend ]
        customerValue = [ sub['newcustomer'] for sub in newcustomerstrend ]
        customerHasBK = [ sub['countbk'] for sub in newcustomerstrend ]

        sql = """
             select c.customerid, cast(sum(b.total_amount) as signed) as topsales
                from bookings b
                left join customers c on c.customerid = b.customerid
                where booking_date between %s and %s
                group by c.customerid
                order by sum(total_amount) desc
                limit 5
            """
        cursor.execute(sql, parameters_date)
        salestop5 = cursor.fetchall()
        customerids = [ sub['customerid'] for sub in salestop5 ]
        topsales = [ sub['topsales'] for sub in salestop5 ]

        return render_template("report_customers.html", newcustomers=newcustomers, ticektpercus=ticektpercus, salespercus=salespercus, ticketsales_num=ticketsales_num, giftcard_num=giftcard_num,\
                               top5names=top5names, top5values=top5values, customerWeek=customerWeek,customerValue=customerValue,customerHasBK=customerHasBK, customerids=customerids, topsales=topsales)
    else:
        flash("Please login as manager or admin", "warning")
        return redirect(url_for('staff_login.stafflogin'))

