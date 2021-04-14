CS50w - Capstone Project 

Designing and implementing a web application of your own with Python and JavaScript.

## Overview

The final project is your opportunity to design and implement a dynamic website of your own. So long as your final project draws upon this course’s lessons, the nature of your website will be entirely up to you.


## Requirements
In this project, you are asked to build a web application of your own. The nature of the application is up to you, subject to a few requirements:

- Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
- Your web application must be mobile-responsive.
- In a README.md in your project’s main directory, include a short writeup describing your project, what’s contained in each file you created, and (optionally) any other additional information the staff should know about your project. This file should also provide your justification for why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
- If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!
- Beyond these requirements, the design, look, and feel of the website are up to you!


## Initialization
 - install dependencies with [pip install -r requirements.txt]
 - Make migrations with python manage.py makemigrations.
 - Apply migrations with python manage.py migrate.
 - Create superuser with python manage.py createsuperuser.
 - You can populate the database with menu items from by running python populate_db.py

 ## Database Models
 Room - registered users can create and join rooms with other players, this model contains the attributes to host a room such as initial cash value, max number of players, and date created

 Membership - model that links a user to a room. includes attributes such asset values (cash and stocks), user name and room name, a boolean for if this member is room admin, and their rank in the game. 
 
 Transactions - a model that records all purchases made by a member of a room. includes membership info, stock ticker, quantity, purchase price, and initial purchase date. 
 
 Saved Stock - registered users have the option to save stock to a account and track their performance from the initial date. model records the user info, the ticker, the date added, and the initial price


 ## Files
 stock_app/stocks/views.py contains the backend data query and processing functions to retrieve and present the stock data for users. 

 stock_app/stocks/urls.py provides url path structure for application for user to access each page in application

 stock_app/stocks/static/ contains the js and html files for the overall functionality of the project
 	--> JS
 		-- base.js - open and closing navigation bar in all pages
 		-- create_game.js - function to make request to application to create a new game on user submit. on request reply, document will be updated with a message
 		-- index.js - functions to get current stock quote from application and adding resulting stock quote data to user portfolio. 
 		-- join-game.js - function for user to make join game request
 		-- portfolio.js - functions to toggle selecting checkboxes in user saved stock portfolio, removing all saved stocks from portfolio, and making a request to application to remove saved stock data from table 
 	--> HTML
 		-- base - Base HTML template for application
 		-- buy-sell - user can finalize a transaction in a room
 		-- create-game - user can create a new game room
 		-- game-portfolio - portfolio for users stocks per game room
 		-- game - lobby page for each game
 		-- index - home page for application, user can lookup stocks, and go to joined games if signed in
 		-- join-game - page to view games user can join
 		-- login - user login page
 		-- portfolio - see all stocks saved and tracked by user
 		-- register - user registration page
 		-- transaction - transaction confirmation page for user transactions


