from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Email libs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from helpers import login_required


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///booking.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create Admin
"""
adminN = "Admin"
adminHash = generate_password_hash("admin1")
db.execute("INSERT INTO admin (adminName, hash) VALUES (?, ?)", adminN, adminHash)
"""

@app.route("/")
def index():

    session.clear()
    session["accountType"] = None
    return redirect("/home")


# I've difined an specific route called home to be able to define accountType in the root one
@app.route("/home")
def home():

    return render_template("home.html")


@app.route("/media")
def media():

    return render_template("media.html")


@app.route("/guide")
def guide():

    return render_template("guide.html")


@app.route("/area")
def area():

    return render_template("area.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact"""
    # If user already loged id autocomplete name and email fields
    if "user_id" in session:
        userInfo = db.execute("SELECT name, email FROM users WHERE id = ?", session["user_id"])
    else:
        userInfo = None

    if request.method == "POST":

        # Send e-mail to self del cobre's mail
        name = request.form.get("name")
        email_address = request.form.get("email")
        email_subject = request.form.get("subject")
        email_subject = name + ': ' + email_subject
        email_message = email_address + ' sent you a message: "' + request.form.get("message") + '"'

        sender_email = 'delcobreclimbing@gmail.com'
        sender_password = 'DOLJZVVOMRTHXTOQ'
        receiver_email = 'delcobreclimbing@gmail.com'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = email_subject
        message.attach(MIMEText(email_message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            # Confirm the user that message has been sended
            flash("Thanks for your message")

            return redirect("/contact")
        except Exception as e:
            return str(e)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("contact.html", userInfo=userInfo)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Check availabilty of username
        if db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            alert("The username is already in use")
            return redirect("/register")

        # Check that password and confirmation are equals
        elif request.form.get("password") != request.form.get("confirmation"):
            alert("Pasword and pasword confirmation are diferent")
            return redirect("/register")

        # If everything is ok, proceed to store values into db
        else:
            username = request.form.get("username")
            name = request.form.get("name")
            lastName = request.form.get("lastName")
            email = request.form.get("email")
            password = request.form.get("password")
            hash = generate_password_hash(password)

            db.execute("INSERT INTO users (username, name, lastName, email, hash) VALUES (?, ?, ?, ?, ?)",
                       username, name, lastName, email, hash)

            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["accountType"] = "user"

            # Send a confirmation for the register to the user
            email_subject = name + ": You've been registered"
            email_message = 'Hello ' + name + ',\nthanks for your register at Del cobre climbing Camping.\n Your user name is: ' + username +'\n\nDel cobre climbing team.'

            sender_email = 'delcobreclimbing@gmail.com'
            sender_password = 'DOLJZVVOMRTHXTOQ'
            receiver_email = email

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = email_subject
            message.attach(MIMEText(email_message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

        # Redirect user to camping page
            return redirect("/camping")
        except Exception as e:
            return str(e)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password")
            return render_template("camping.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["accountType"] = "user"

        # Redirect user to camping page
        return redirect('/camping')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/camping", methods=["GET", "POST"])
def camping():

    # Redirect admin user to Admin page to see bookings history
    if session["accountType"] == "admin":
        return redirect("/admin")

    # In case of user's active session query the db to be able to show the booking
    if "user_id" in session:
        booked = db.execute("SELECT * FROM booking WHERE userID = ?", session["user_id"])
    else:
        booked = False

    # In case of POST method
    if request.method == "POST":
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        number = request.form.get("number")

        # Check for valid Date values
        # Check that start Date is from today and ahead
        currentDate = datetime.today().strftime('%Y-%m-%d')
        if startDate < currentDate:
            # Notify the user
            flash("You have selected an invalid start date")
            return render_template("camping.html")

        # Check that firstDate is < endDate

        elif startDate > endDate:
            # Notify the user
            flash("Start date must be before the end date")
            return render_template("camping.html")

            # Check that number is number
        elif not number.isdecimal():
            # Notify the user
            flash("You have selected an invalid number of persons")
            return render_template("camping.html")

        # Store data into DB
        db.execute("INSERT INTO booking (userID, startDate, endDate, number, timestamp) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], startDate, endDate, number, currentDate)
        booked = db.execute("SELECT * FROM booking WHERE userID = ?", session["user_id"])

        # Send an E-mail confirmation of the booking to the user
        # Query to DB to get information of the active user
        userInfo = db.execute("SELECT username, name, lastName, email FROM users WHERE id = ?", session["user_id"])

        name = userInfo[0]["name"]
        lastName = userInfo[0]["lastName"]
        email_address = userInfo[0]["email"]
        email_subject = name + ": Your booking at Del cobre climbing"
        email_message = name + ' ' + lastName + ",\n Thanks for your booking at Mogotabo's camping area.\n By camping here, you contribuite to the community's economical and social developement.\n\nYour booking:\nStart date: " + startDate + '\nEnd date: ' + endDate + '\nNumber of persons: ' + number + '\n\n If you have any questions about your booking you can replay this email or contact us trought the contact page in our website.\n\n Del cobre climbing team.'

        sender_email = 'delcobreclimbing@gmail.com'
        sender_password = 'DOLJZVVOMRTHXTOQ'
        receiver_email = email_address

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = email_subject
        message.attach(MIMEText(email_message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            # Flash booking confirmation
            flash("Thanks for your booking")

            return redirect("/camping")
        except Exception as e:
            return str(e)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("camping.html", booked=booked)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # Handling a delete from user's interface
    if session["accountType"] == 'user':
        db.execute("DELETE FROM booking WHERE userID = ?", session["user_id"])
        return redirect('/camping')

    # Handling a delete from admin's interface
    else:
        bookingID = request.form.get('bookingID')
        db.execute("DELETE FROM booking WHERE id = ?", bookingID)
        return redirect('/admin')


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    # If not Admin redirect user to camping page
    if session["accountType"] == "user":
        return redirect("/camping")

    if request.method == "POST":

        # Query database for adminname
        rows = db.execute(
            "SELECT * FROM admin WHERE adminName = ?", request.form.get("adminName")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
            ):
            flash("Invalid admin and/or password")
            return render_template("admin.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["accountType"] = "admin"

        # Return redirect("/admin")
        bookings = db.execute(
            "SELECT booking.id, users.username, users.name, users.lastName, users.email, booking.startDate, booking.endDate, booking.number, booking.timestamp FROM booking JOIN users ON booking.userID = users.id;")
        return render_template("admin.html", bookings=bookings)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        bookings = db.execute(
            "SELECT booking.id, users.username, users.name, users.lastName, users.email, booking.startDate, booking.endDate, booking.number, booking.timestamp FROM booking JOIN users ON booking.userID = users.id;")
        return render_template("admin.html", bookings=bookings)


@app.route("/adminBook", methods=["POST"])
def adminBook():
    """ Handles a booking from de Admin page"""
    # Store inputs into variables
    name = request.form.get("name")
    email = request.form.get("email")
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")
    number = request.form.get("number")

    # Check in Data base that user is correct

    userInfo = db.execute("SELECT id FROM users WHERE name = ? AND email = ?", name, email)

    if not userInfo:
        print("Checking null")
        flash("Incorrect name or email")
        return redirect("/admin")

    #Check if a booking for the user already exists
    booked = db.execute("SELECT * FROM booking WHERE userID = ?", userInfo[0]["id"])
    if booked:
        flash("There's an existing Booking for this user")
        return redirect("/admin")

    # Check for valid Date values
    # Check that start Date is from today and ahead
    currentDate = datetime.today().strftime('%Y-%m-%d')
    if startDate < currentDate:
        # Notify the user
        flash("You have selected an invalid start date")
        return redirect("/admin")

    # Check that firstDate is < endDate

    elif startDate > endDate:
        # Notify the user
        flash("Start date must be before the end date")
        return redirect("/admin")

        # Check that number is number
    elif not number.isdecimal():
        # Notify the user
        flash("You have selected an invalid number of persons")
        return redirect("/admin")

    # Store data into DB
    db.execute("INSERT INTO booking (userID, startDate, endDate, number, timestamp) VALUES (?, ?, ?, ?, ?)",
                userInfo[0]["id"], startDate, endDate, number, currentDate)

    # Send an E-mail confirmation of the booking to the user
    # Query to DB to get information of the active user
    userInfo = db.execute("SELECT username, name, lastName, email FROM users WHERE id = ?", session["user_id"])


    lastName = userInfo[0]["lastName"]
    email_address = email
    email_subject = name + ": Your booking at Del cobre climbing"
    email_message = name + ' ' + lastName + ",\n Thanks for your booking at Mogotabo's camping area.\n By camping here, you contribuite to the community's economical and social developement.\n\nYour booking:\nStart date: " + startDate + '\nEnd date: ' + endDate + '\nNumber of persons: ' + number + '\n\n If you have any questions about your booking you can replay this email or contact us trought the contact page in our website.\n\n Del cobre climbing team.'

    sender_email = 'delcobreclimbing@gmail.com'
    sender_password = 'DOLJZVVOMRTHXTOQ'
    receiver_email = email_address

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        # Flash booking confirmation
        flash("Booking successful")

        return redirect("/admin")
    except Exception as e:
        return str(e)