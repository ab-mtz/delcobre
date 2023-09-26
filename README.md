# Del Cobre Climbing
#### Video Demo: [Watch Video](https://youtu.be/ErzYpNofCEU)
#### Description:

This website is created for a project called Del Cobre Climbing, a personal climbing and social project in Mexico. The main objective is to apply the knowledge acquired during the CS50 course to address real-life problems.

Del Cobre Climbing involves the development of a climbing area in the lands of a Tarahumara community known as Mogotabo. The project aims to attract tourists to the area, contributing to the local economy and social development. As part of this initiative, a camping area has been established where tourists can stay, injecting money directly into the community and creating a shared space for both locals and visitors. To facilitate reservations for this camping area, a booking system has been incorporated into the Del Cobre Climbing website.

The backend of the website is written in Python using the Flask framework, while the frontend mainly consists of HTML, CSS, JINJA2 syntax, some Bootstrap features, and JavaScript to enhance the user interface. All the managed information is stored in a SQLite 3 database.

The booking functionality is accessible through the "Camping" page. Non-logged-in users initially see the option to register or log in. Once a user registers, they receive a personalized email confirmation using the SMTP and MIMEMultipart libraries and are redirected back to the Camping page while remaining logged in. On the Camping page, a booking reservation form is displayed, allowing users to select their desired dates and the number of persons. After making a reservation, users receive a booking confirmation email. If a user already has an existing booking and is logged in, they will see their booking details instead of the booking form.

Another significant feature on the website is designed for the camping administrator, who can log in using the following credentials:

Admin Name: Admin
Password: admin1

Once logged in, the admin can view the booking information of all users, including full user details and booking information. The admin also has the ability to delete a booking and create a new one. When a new booking is made, the user is notified by email, and the admin is also notified when a new message is sent.

### DOCUMENTS

- TEMPLATES
	- admin.html
	This document displays the admin page, including code to display messages coming directly from the backend using the flash function. It checks for an active session, and if it's not an admin session, users are automatically redirected to the "/camping" route to protect other users' information. If it's an admin session, the page displays the history of bookings stored in the database. Each booking has a button for deletion (calling the "/delete" route) and the ability to add a new booking through the "/adminBook" route. When a new booking is created, the user is notified by email.

	- area.html
	This document is an informative page that includes an embedded Google Map, allowing users to explore the area.

	- camping.html
	This document shows the Camping page, which has the most incorporated functionalities. It includes code to display messages from the backend through the flash function. It checks for an active session and, if it's an admin session, redirects to the "/admin" route. Otherwise, it displays options for users to register or log in. Once registered or logged in, the Camping page allows users to create a booking by selecting start and end dates and the number of persons. If the user is already logged in and has made a booking, the page displays the existing booking and provides a button for deletion. If the user wants to modify the current booking, they must delete the current one and create a new one. The page also includes a logout option.

	- contact.html
	This page allows users to send a message to the admin's email. Upon accessing the page, users see a hero-style page with a "contact" button. Clicking the button opens a modal with a form to write a message. The modal is implemented using Bootstrap and JavaScript. If the user is logged in, the name and email fields are pre-filled; otherwise, they appear empty. There's also a close button to cancel the message and a send button to send the message to the admin's email. A confirmation message appears when the message is sent.

	- guide.html
	This page displays an embedded PDF containing information about the climbing crags developed in the area.

	- home.html
	The Home page provides general information about the project, along with related images.

	- layout.html
	This document serves as the general layout for other HTML pages and includes the header and shared characteristics like the title and navigation bar.

	- login.html
	This page is for user login, referring to the "/login" route. It checks the validity of the user's input data.

	- media.html
	This page contains two embedded YouTube videos using iframe tags, which are two short documentaries about the project.

	- register.html
	In this page, users can register for the system by providing their personal information, including name, last name, username, email, and password. After a successful registration, the user receives an email confirmation with their username information.

- STATIC
	In this folder, you can find the images used in the website.

	- styles.css
	This document contains the CSS styles used on the website.

- app.py
This file contains all the backend implementation and logic of the website, using Python with the Flask framework. After defining the necessary libraries and configuring the application, database, and sessions, there are 13 routes:

	- "/"
	This is the first access route where any session information is cleared, and a variable called "accountType" is defined as None to control user and admin access. After that, it redirects to the "/home" route.

	- "/home"
	Returns the template for home.html.

	- "/media"
	Returns the template for media.html.

	- "/guide"
	Returns the template for guide.html.

	- "/area"
	Returns the template for area.html.

	- "/contact"
	- If GET: Returns the template for contact.html.
	- If POST: Manages the information from the contact form, sending an email with the user's information and message to the admin, and provides a flash confirmation to the user that the message has been sent.
	Returns the template for home.html.

	- "/register"
	Handles the registration of a new user. Checks that the input data is valid and that the user doesn't already exist in the database. After a successful registration, it sends an email confirmation to the provided address and redirects to "/camping."

	- "/login"
	Handles user login by checking the validity of inputs in the database. After a successful login, it redirects the user to "/camping."

	- "/camping"
	Here, most of the booking functions are implemented. It checks that all the input data for a new booking is correct, stores it in the database, and sends a confirmation email to the user.

	- "/delete"
	Handles the deletion of a booking by either the user or the admin. It then redirects to the origin of the action.

	- "/logout"
	Handles user or admin logout and redirects to "/home."

	- "/admin"
	Handles the admin login, checking the validity of input in the database

###After logging in, it displays the bookings stored in the database along with user information.

	- "/adminBook"
	Handles the booking request initiated by the admin and sends an email confirmation to the user.

- booking.db
This database stores information about users, admins, and bookings.

### SCHEMA:

´´´sql
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
FOREIGN KEY (userID) REFERENCES users(id),
UNIQUE (id)
);

CREATE TABLE admin (
id INTEGER,
adminName TEXT,
hash TEXT NOT NULL
);
´´´

- helpers.py
This file provides functions for app.py, like "login_required."

### DESIGN CHOICES

####At the beginning of the project, I wasn't sure how to best implement the booking function on the site, such as how many HTML documents to use or how many routes to implement in the backend. I tried to include the most functionalities in fewer HTML documents and implement some logic with Jinja syntax to display certain content based on conditions in the backend. I also used routes with shared functions for actions coming from both the user and admin interfaces, like the logout route or the delete booking route.

Additionally, due to my lack of experience in database design, I had to redesign the database of my project when I realized I needed to store more fields.


I have made several corrections and improvements to the text for clarity and consistency. Please feel free to use this revised version as needed.
