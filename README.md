# Delcobreclimbing
#### Video Demo:  <https://youtu.be/ErzYpNofCEU>
#### Description:

This is a website for a project called Del Cobre Climbing, which is a personal Climbing-Social project in Mexico. The idea is to translate some of the knowledge acquired in the CS50 course to real-life problems.

In general terms, Del Cobre Climbing involves the development of a climbing area in the lands of a Tarahumara community called Mogotabo. The goal is to attract tourism to the area, contributing to the local economy and social development. One part of the project involves the development of a camping area where tourists can stay, injecting money directly into the community and creating a common space for the local people and visitors. To facilitate this, I have incorporated a booking system into the Del Cobre Climbing's informative website, allowing potential visitors to book a place in the camping area.

The backend is written in Python using the Flask framework. The frontend mainly consists of HTML, CSS, JINJA2 syntax, some Bootstrap features, and JavaScript to enhance the user interface. All the managed information is stored in a database using SQLite 3.

The booking function operates through the "camping" page, where non-logged-in users initially see the option to register or log in. Once a user has registered, they receive a personalized email confirmation using smtp and MIMEMultipart libraries and are redirected back to the camping page while remaining logged in. On the camping page, a booking reservation form is displayed, allowing users to select their desired dates and the number of persons. After making a reservation, users receive a booking confirmation email. If a user already has an existing booking and is logged in, they will see their booking details instead of the booking form.

Another important feature on the website is designed for the camping administrator, who can log in using a pre-defined admin name and password:

Admin Name: Admin
Password: admin1

Once logged in, the admin can view the booking information of all users, including full user details and booking information. The admin also has the ability to delete a booking and create a new one. When a new booking is made, the user is notified by email.

The admin is notified by email when a user has made a new booking and when a new message has been sent.

DOCUMENTS

-TEMPLATES
	-admin.html
	This document shows the admin page. At first whit jinja2 syntax there's the code to be able to display a mesage comming directly from the backend trough a flash function.
	Once start displayin the content of the body, using again jinja 2 sytax, it'll check if there is an active sesion (the backend will check if the sesion is for admin or user, if is not admin, the user will be automatically redirected to the "/camping" route protectig other users info),
	if not, it will display the Log in formular, otherwise it will show the history of bookings that are stored in the DB. There's a button next to each register to be able
	to delete it (Calling the route "/delete") and as well the posibility to add a new booking through the route "/adminBook". When a new booking is created the user will be notified by e-mail.

	-area.html
	This document is just an informative page, where an Embeded Map from Google allow the user to explore the area.

	-camping.html
	This document shows the camping page wich is the one that has the more incorporated functionalities. At first whit jinja2 syntax there's the code to be able to display a mesage comming directly from the backend trough a flash function.
	Once start displayin the content of the body, using again jinja 2 sytax, it'll check if there is an active sesion (the backend will check if the sesion is for admin or user, if is an Admin will be redirected to the "/admin" route),
	if not, it will display two tags to make a Register or Log In, each of this will redirect the user to the respectives pages.
	Once the user has registered or loged in, the camping page will display the option to create a booking selecting the start and end dates of the booking, and the number of persons.
	If the user log in and has already booked, the page won't show the booking formular, instead it will show the booking made and a button to delete the booking. If the user wants to modify the current booking will need to delate the current one and make a new one.
  	There is a tag as well to log out.

	-contact.html
	This page gives the user the possibility to send a message to the admin's email, once the user access will only see a hero style page with the button "contact" that when clicked it will display
	a modal with a formular in it to write a message. The modal has been implemented using bootstraps and JavaScript. If the user is loged in, the fields name and email will be already filled, otherwise they'll appear empty.
	There's a close button in the case that the user doesn't want to send the message anymore. And a send button. When clicked, if all the fields are filled, it will send an email to the admin's email, and show a confirmation that the message has been sent.

	-guide.html
	This page will display an embedded PDF wich cointains information about the climbing crags already developed in the area.

	-home.html
	This is the home page where the user will see some general information about the project with some pictures related to it.

	-layout.html
	This document is the general layout to the other html's that cointains header and part of the body's shared characteristics, like the titel and navigation bar.

	-login.html
	This is the log in page for the users that refers to the route "/login" that will check the validity of the data typed by the user.

	-media.html
	This page contains two embedded youtube videos using iframe tag that are two short documentaries of the project.

	-register.html
	In this page the user will be able to register to the system typing their personal information such as name, last name, username and e-mail, and could create a password.
	After a succesful register, the user will recieve an e-mail confirmation with their username info.

-STATIC
	In this folder finds the images used in the website

	-styles.css
	This document contains the css styles used in the website.

-app.py
Here is all the backend implementation and logic of the website. Using Python with the framework Flask.
After definied the necessary libraries and configuring application, database and sessions, there are 13 routes.

	-"/"
	It's the first accesd route where any session info is cleared and a variable called accountType is defined as None, to help us to control who can access the users or admins page. After that, redirects to the "/home" route.

	-"/home"
	Returns the template of home.html

	-"/media"
	Returns the template of media.html

	-"/guide"
	Returns the template of guide.html

	-"/area"
	Returns the template of area.html

	-"/contact"
	If GET : Returns the template of contact.html
	If POST: manage the info from the contact formular sending an email with the info of the user and it's message to the admin,
	and a flash confirmation to the user that the message has been sent.
	Returns the template of home.html

	-"/register"
	Handles the register of a new user.
	Check that the input data is valid and that the user doesn't already exist on the database.
	After a successful register, sends an e-mail confirmation to the given address.
	Redirects to "/camping"

	-"/login"
	Handles the log in of the users. Checking the validity of inputs  in the database.
	After a succesful log in, redirect the user to "/camping"

	-"/camping"
	Here are implemented most of the booking functions, it checks that all the input data for a new booking are correct and stores it
	into the database and send a confirmation e-mail to the user.

	-"/delete"
	Handles the delete function of a booking coming from the user or the Admin.
	Redirects to the origin of the action.

	-"/logout"
	Handles the log out from user or admin and redirects to "/home".

	-"/admin"
	Handle the Admin login checking the validity of input in the datbase.
	After loged in, displays the Bookings stored in the database with the info of the user.

	-"/adminBook"
	Handles the booking request coming from the admin and send an e-mail confirmation to the user.

-booking.db
Stores the information of the users, admins and bookings.

SCHEMA:

CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL UNIQUE,
name TEXT NOT NULL,
lastName TEXT NOT NULL,
email TEXT NOT NULL,
hash TEXT NOT NULL
);

CREATE TABLE booking(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
userID INTEGER,
startDate TEXT,
endDate TEXT,
number INTEGER,
timestamp TEXT,
FOREIGN KEY (userID) REFERENCES users(id)
UNIQUE (id)
);

CREATE TABLE admin (
id INTEGER,
adminName TEXT,
hash TEXT NOT NULL
);

-helpers.py
It provides functions to the app.py like login_required


DESIGN CHOICES


At the begining of the project I wasn't sure how was better to implement the booking function in the site, like how many html documents should I use, or how many routes implement in the backend.
I tried to include the more functionalities in fewer html documents and implement some logics with Jinja syntaxis, and displain certain content depending on conditions happening in the backend.
I also tried to use some routes with shared functions for two same actions comming from the user or admin interface, for example the log out route or the delete booking route.

As well because of my lack of experience into data base design I had to re-design the database of my project when I realized that I needed to store more or less fields.

