DROP DATABASE `group4lincoln$moviemagic`;
CREATE DATABASE `group4lincoln$moviemagic`;
USE `group4lincoln$moviemagic`;

-- cinemas table
CREATE TABLE IF NOT EXISTS cinemas
(
	cinemaid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);


-- tickets table
CREATE TABLE IF NOT EXISTS tickets 
(
	ticketid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ticket_type VARCHAR(20) NOT NULL,
    price FLOAT NOT NULL,
    is_fixed BOOLEAN NOT NULL DEFAULT 0 -- if it is tuesday discount, = 1 

);

-- promotion types
CREATE TABLE IF NOT EXISTS promotion_types
(
	promotion_type_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    promotion_type VARCHAR(20) NOT NULL,
    descriptions VARCHAR(50) NOT NULL
)
;

-- promotions table
CREATE TABLE IF NOT EXISTS promotions
(
	promotionid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    promotion_code VARCHAR(20),
    effective_date DATETIME NOT NULL,
    expiration_date DATETIME NOT NULL,
    promotion_type_id INT NOT NULL, 
    title VARCHAR(30) NOT NULL,
    descriptions VARCHAR(100) NOT NULL,
    details TEXT NOT NULL,
    image TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (promotion_type_id) REFERENCES promotion_types(promotion_type_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- giftcard types, dim table
CREATE TABLE IF NOT EXISTS giftcard_types
(
	giftcard_type_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    giftcard_name VARCHAR(30) NOT NULL,
    image TEXT NOT NULL
)
;


-- roles table
CREATE TABLE IF NOT EXISTS roles
(
	roleid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    role VARCHAR(15) NOT NULL
);

-- create accounts table that holds username (email, password)
CREATE TABLE IF NOT EXISTS accounts
(
	accountid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL, -- EMAIL ADDRESS
    password VARCHAR(255) NOT NULL,
    roleid INT NOT NULL,
    FOREIGN KEY (roleid) REFERENCES roles(roleid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- create customers table
CREATE TABLE IF NOT EXISTS customers
(
	customerid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    is_active VARCHAR(20) NOT NULL DEFAULT 1,
    accountid INT NOT NULL,
    join_date DATE NOT NULL,
    FOREIGN KEY (accountid) REFERENCES accounts(accountid) ON UPDATE CASCADE ON DELETE CASCADE
);
-- staff table
CREATE TABLE IF NOT EXISTS staff
(
	staffid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    is_active VARCHAR(20) NOT NULL DEFAULT 1,
    accountid INT NOT NULL,
    join_date DATE NOT NULL,
    FOREIGN KEY (accountid) REFERENCES accounts(accountid) ON UPDATE CASCADE ON DELETE CASCADE
);

/*
CREATE TABLE IF NOT EXISTS managers
(
	managerid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    is_active VARCHAR(20) NOT NULL DEFAULT 1,
    accountid INT NOT NULL,
    join_date DATE NOT NULL,
    FOREIGN KEY (accountid) REFERENCES accounts(accountid) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS admins
(
	adminid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    is_active VARCHAR(20) NOT NULL DEFAULT 1,
    accountid INT NOT NULL,
    join_date DATE NOT NULL,
    FOREIGN KEY (accountid) REFERENCES accounts(accountid) ON UPDATE CASCADE ON DELETE CASCADE
);
*/

-- giftcards table, balance can be calculated by joining bookings table
CREATE TABLE IF NOT EXISTS giftcards
(
	giftcardid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    giftcard_number VARCHAR(16) NOT NULL,
    giftcard_value INT NOT NULL,
    giftcard_type_id INT NOT NULL,
    customerid INT NOT NULL,

    FOREIGN KEY (giftcard_type_id) REFERENCES giftcard_types(giftcard_type_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (customerid) REFERENCES customers(customerid) ON UPDATE CASCADE ON DELETE CASCADE

);

-- genre table

CREATE TABLE IF NOT EXISTS genre
(
	genreid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    genre_name VARCHAR(20) NOT NULL,
    created_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    updated_date DATE NOT NULL DEFAULT (CURRENT_DATE)
);

-- genre table

CREATE TABLE IF NOT EXISTS ratings
(
	ratingid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    rating_code VARCHAR(10) NOT NULL,
    color VARCHAR(20) NOT NULL,
    created_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    updated_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    descriptions VARCHAR(100) NOT NULL
);

-- actors table

CREATE TABLE IF NOT EXISTS actors
(
	actorid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(25) NOT NULL,
    lastname VARCHAR(25) NOT NULL,
    actor_name VARCHAR(52) NOT NULL,
    created_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    updated_date DATE NOT NULL DEFAULT (CURRENT_DATE)
);


-- movies table

CREATE TABLE IF NOT EXISTS movies
(
	movieid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    start_date DATE NOT NULL,
    descriptions TEXT NOT NULL,
    runtime_hour INT NOT NULL,
    runtime_minute INT NOT NULL,
    genreid INT NOT NULL,
    ratingid INT NOT NULL,
    image_url TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (genreid) REFERENCES genre(genreid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ratingid) REFERENCES ratings(ratingid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- starring table for bridging actors and movies

CREATE TABLE IF NOT EXISTS starring
(
	starringid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    movieid INT NOT NULL,
    actorid INT NOT NULL,
    latest_version BOOL NOT NULL DEFAULT TRUE,
    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (actorid) REFERENCES actors(actorid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- dates table

CREATE TABLE IF NOT EXISTS dates
(
	dateid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    weekday_number INT NOT NULL,
    weekday_name VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS sessiontime 
(
	sessiontime_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    sessiontime TIME NOT NULL,
    maximum_time TIME NOT NULL,
    -- next_sessiontime_id INT,
    cinemaid INT NOT NULL,
    FOREIGN KEY (cinemaid) REFERENCES cinemas(cinemaid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- sessions table, using which we can find movie & cinema details, joining with bookings

CREATE TABLE IF NOT EXISTS sessions
(
	sessionid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    session_date DATE NOT NULL,
    sessiontime_id INT NOT NULL,
    -- session_week_no INT NOT NULL, -- get it from dates
    -- session_week_name VARCHAR(15) NOT NULL, -- get if from dates
    movieid INT NOT NULL,
    -- cinemaid INT NOT NULL, -- from session time
    FOREIGN KEY (movieid) REFERENCES movies(movieid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (sessiontime_id) REFERENCES sessiontime(sessiontime_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- seats table, for populating bookings table

CREATE TABLE IF NOT EXISTS seats
(
	seatid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    seat_number VARCHAR(10) NOT NULL,
    cinemaid INT NOT NULL,
    FOREIGN KEY (cinemaid) REFERENCES cinemas(cinemaid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- bookings table, customer, giftcard, promotion, session info are included at booking order level
-- net amount = total amount - promotion

CREATE TABLE IF NOT EXISTS bookings
(
	bookingid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    booking_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    booking_time TIME NOT NULL DEFAULT (CURRENT_TIME),
    no_of_tickets INT NOT NULL,
    total_amount FLOAT NOT NULL,
    -- net_amount FLOAT NOT NULL, -- total amount - promotion
	giftcardid INT DEFAULT NULL,
    giftcard_deducted FLOAT DEFAULT 0,
    payment_amount FLOAT DEFAULT 0,
    customerid INT NOT NULL,
    sessionid INT NOT NULL,
	promotion_deducted FLOAT DEFAULT 0,
    promotionid INT DEFAULT NULL,
    FOREIGN KEY (customerid) REFERENCES customers(customerid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (promotionid) REFERENCES promotions(promotionid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (giftcardid) REFERENCES giftcards(giftcardid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (sessionid) REFERENCES sessions(sessionid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- bridging table for booking and seats

CREATE TABLE IF NOT EXISTS booking_seats
(
	bsid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    bookingid INT NOT NULL,
    seatid INT NOT NULL,
    is_checkin BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (bookingid) REFERENCES bookings(bookingid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (seatid) REFERENCES seats(seatid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- booking transactions table, ticket types and number of tickets are included at order-line/transaction level

CREATE TABLE IF NOT EXISTS booking_transactions
(
	transactionid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    transaction_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    transaction_time TIME NOT NULL DEFAULT (CURRENT_TIME),
    no_of_tickets INT NOT NULL,
    unit_price FLOAT NOT NULL,
    -- total_ticket_amount FLOAT NOT NULL,
    bookingid INT NOT NULL,
    ticketid INT NOT NULL,
    FOREIGN KEY (bookingid) REFERENCES bookings(bookingid) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (ticketid) REFERENCES tickets(ticketid) ON UPDATE CASCADE ON DELETE CASCADE
    
);

-- payment table, giftcard will be entered when making the payment

CREATE TABLE IF NOT EXISTS payment
(
	paymentid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    amount FLOAT NOT NULL,
    payment_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    payment_time TIME NOT NULL DEFAULT (CURRENT_TIME),
    payment_type VARCHAR(30) NOT NULL, # giftcard, or booking
    customerid INT NOT NULL,
    bookingid INT, 
    FOREIGN KEY (customerid) REFERENCES customers(customerid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (bookingid) REFERENCES bookings(bookingid) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS giftcard_payment
(
	gpid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    giftcardid INT NOT NULL,
	paymentid INT NOT NULL,
    FOREIGN KEY (paymentid) REFERENCES payment(paymentid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (giftcardid) REFERENCES giftcards(giftcardid) ON UPDATE CASCADE ON DELETE CASCADE
);

-- ticket price to existing promotion
CREATE TABLE IF NOT EXISTS ticket_promotion
(
	tpid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    original_price FLOAT NOT NULL,
    discounted_price FLOAT DEFAULT NULL,
    discount_percentage FLOAT DEFAULT NULL,
    ticketid INT NOT NULL,
    promotionid INT NOT NULL,
    latest_version BOOLEAN NOT NULL DEFAULT TRUE,
    is_percentage BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (ticketid) REFERENCES tickets(ticketid) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (promotionid) REFERENCES promotions(promotionid) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company
(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(30) NOT NULL,
    country VARCHAR(25) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    latest_version BOOLEAN NOT NULL DEFAULT TRUE,
    created_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    updated_date DATE NOT NULL DEFAULT (CURRENT_DATE)
)
;
/*
CREATE TABLE IF NOT EXISTS contact_message
(
	sendid INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fullname VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    message VARCHAR(200) NOT NULL,
    send_datetime DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
)
;
*/

-- company information
INSERT INTO company
VALUES
(1, '098887777', 'ContactUs@MovieMagic.com',
'2023 Magic Road', 'Rolleston', 'New Zealand', '2023', 1, '2020-02-20', '2020-02-20')
;
-- insert data to roles table
INSERT INTO roles 
VALUES
(1, 'admin'),
(2, 'manager'),
(3, 'staff'),
(4, 'customer');

-- insert data to cinemas
INSERT INTO cinemas
VALUES
(1, 'One Piece'),
(2, 'Two Events'),
(3, 'Three Trees'),
(4, 'Big Four');

-- insert data to ratings table
INSERT INTO ratings 
VALUES
(1, 'G', 'green', '2021-01-01', '2021-01-01', 'Suitable for general audiences of all ages.'),
(2, 'PG', 'yellow', '2021-01-01', '2021-01-01', 'Younger children may require parental guidance.'),
(3, 'M', 'yellow', '2021-01-01', '2021-01-01', 'Suitable for mature persons over 16 years of age.'),
(4, 'R13', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 13 years of age only.'),
(5, 'R15', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 15 years of age only.'),
(6, 'R16', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 16 years of age only.'),
(7, 'R18', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 18 years of age only.'),
(8, 'RP13', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 13 years of age unless accompanied by a parent or guardian.'),
(9, 'RP16', 'red', '2021-01-01', '2021-01-01', 'Restricted to persons over 16 years of age unless accompanied by a parent or guardian.'),
(10, 'R', 'red', '2021-01-01', '2021-01-01', 'Special Restriction refer to the text beside the label for the full restriction.'),
(11, 'E', 'yellow', '2021-01-01', '2021-01-01', 'Exempt from classification.');

-- insert data to genre
INSERT INTO genre 
VALUES
(1, 'Action', '2021-01-01', '2021-01-01'),
(2, 'Adventure', '2021-01-01', '2021-01-01'),
(3, 'Animated', '2021-01-01', '2021-01-01'),
(4, 'Comedy', '2021-01-01', '2021-01-01'),
(5, 'Drama', '2021-01-01', '2021-01-01'),
(6, 'Fantasy', '2021-01-01', '2021-01-01'),
(7, 'Historical', '2021-01-01', '2021-01-01'),
(8, 'Horror', '2021-01-01', '2021-01-01'),
(9, 'Musical', '2021-01-01', '2021-01-01'),
(10, 'Noir', '2021-01-01', '2021-01-01'),
(11, 'Romance', '2021-01-01', '2021-01-01'),
(12, 'Science fiction', '2021-01-01', '2021-01-01'),
(13, 'Thriller', '2021-01-01', '2021-01-01'),
(14, 'Western', '2021-01-01', '2021-01-01'),
(15, 'Family', '2021-01-01', '2021-01-01');

-- ticket data
INSERT INTO tickets
VALUES
(1, 'Adult', 20, 0),
(2, 'Child', 14, 0),
(3, 'Student', 16, 0),
(4, 'Senior', 18, 0),
(5, 'Magic Tuesday', 10, 1)
;

-- expired promotion
-- INSERT INTO promotions
-- VALUES
-- (1, '2023-01-01', '2023-01-07', 'price', '50% OFF WEEK', 'Discount of the Week', 'This week please enjoy the discountged movie offer',
-- 'https://images.unsplash.com/photo-1580828343064-fde4fc206bc6?q=80&w=3271&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D' ),
-- (2, '2023-01-08', '2023-01-14', 'price', '50% OFF WEEK', 'Discount of the Week', 'This week please enjoy the discountged movie offer',
-- 'https://images.unsplash.com/photo-1580828343064-fde4fc206bc6?q=80&w=3271&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D' )
-- ;

-- INSERT INTO ticket_promotion
-- VALUES
-- (1, 20, 10, 50, 1, 1, 0),
-- (2, 14, 7, 50, 2, 1, 0),
-- (3, 16, 8, 50, 3, 1, 0),
-- (4, 18, 9, 50, 4, 1, 0),
-- (5, 20, 10, 50, 1, 2, 0),
-- (6, 14, 7, 50, 2, 2, 0),
-- (7, 16, 8, 50, 3, 2, 0),
-- (8, 18, 9, 50, 4, 2, 0)
-- ;

INSERT INTO giftcard_types
VALUES
(1, 'Golden EGift Card', 
'https://images.unsplash.com/photo-1512916206820-bd6d503c003e?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
),
(2, 'Happy Birthday EGift Card', 
'https://plus.unsplash.com/premium_photo-1673309121075-536e188f8531?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
),
(3, 'Season EGift Card',
'https://plus.unsplash.com/premium_photo-1661760083022-f448a7689738?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
),
(4, 'Valentine EGift Card',
'https://images.unsplash.com/photo-1518414881329-0f96c8f2a924?q=80&w=3289&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
)
;

INSERT INTO promotion_types (promotion_type_id, promotion_type, descriptions)
VALUES
(1, 'tuesday', 'Tuesday Daytime Discount'),
(2, 'price', 'Ticket Price Discount by Promotion Code'),
(3, 'other', 'Non-Price Promotion')
;

INSERT INTO promotions (promotionid, promotion_code, effective_date, expiration_date, promotion_type_id, title, descriptions, details, image, is_active)
VALUES
(1, NULL, '2000-01-01 18:00:00', '9999-12-31 23:59:59', 1, '$10 TUESDAY', 'Tuesday Discount for ALL Movies', 'Movie Magic is offering Tuesday discount on all movies! Only $10 you can enjoy the fun! Just book a movie playing on Tuesday Daytime (7am - 7pm)', 'https://images.unsplash.com/photo-1580828343064-fde4fc206bc6?q=80&w=3271&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 1), 
(2, NULL, '2024-02-09 16:00:00', '2024-02-09 20:00:00', 3, 'Free Popcorn', 'Hurry! Free Popcorn', 'Please enjoy free popcorn when you book a movie showing within promotion effective date. Show your tickets at checked in to one of our staff, and free popcorn will be ready for your movie.', 'https://www.simplyrecipes.com/thmb/bP6MhYxyJ2tCzUY0vfqwb0diMEQ=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Simply-Recipes-Perfect-Popcorn-LEAD-41-4a75a18443ae45aa96053f30a3ed0a6b.JPG', 0), 
(3, 'o6LFwoUri2mrUkMyZJOV', '2024-02-17 10:00:00', '2024-02-17 22:00:00', 2, '20% OFF', 'Hurry! 20% Discount Available', '20% off is now available  at Movie Magic! Just book a movie showing between 17 Feb, 10 am and 17 Feb, 10 pm and enjoy the 20% discount ', 'https://m.media-amazon.com/images/I/51CSzAMBHOL.jpg', 1),
(4, NULL, '2024-02-23 18:00:00', '2024-02-23 22:00:00', 3, 'Games Nights', 'More Games More Fun', 'Please join us in the Game Zone near the receiption at 6 pm. Our game zone is ready to have fun with arcade machines that you will definitely enjoy. ', 'https://images.pexels.com/photos/1293265/pexels-photo-1293265.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 1)
-- (4, '2024-02-24 14:00:00', '2024-02-18 20:00:00', 3, 'Free Drinks', 'Free Drinks for enjoying movies', 'Please enjoy free drinks when you book a movie. Including orange juice, jasmine tea, cola, lemonade and coffe. Please show your ticket at the store when you book a ticket showing on the specified effective date', 'https://st2.depositphotos.com/1875851/7411/i/950/depositphotos_74118935-stock-photo-row-of-various-beverages.jpg', 0)
;

INSERT INTO ticket_promotion (tpid, original_price, discounted_price, discount_percentage, ticketid, promotionid, latest_version, is_percentage)
VALUES
(1, 20, 16, 20, 1, 3, 1, 1),
(2, 14, 11.2, 20, 2, 3, 1, 1),
(3, 16, 12.8, 20, 3, 3, 1, 1),
(4, 18, 14.4, 20, 4, 3, 1, 1)