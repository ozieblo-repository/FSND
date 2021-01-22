Fyyur
-----

> project status : ready for the review \
> **Infosources used during the development and screenshots are included at the end of the ReadMe**

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Overview

This app is nearly complete. It is only missing one thing… real data! While the views and controllers are defined in this application, it is missing models and model interactions to be able to store retrieve, and update data from a database. By the end of this project, you should have a fully functioning site that is at least capable of doing the following, if not more, using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```
> **Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed. 

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


Instructions
-----

1. Understand the Project Structure (explained above) and where important files are located.
2. Build and run local development following the Development Setup steps below.
3. Fill in the missing functionality in this application: this application currently pulls in fake data, and needs to now connect to a real database and talk to a real backend.
3. Fill out every `TODO` section throughout the codebase. We suggest going in order of the following:

  1. Connect to a database in `config.py`. A project submission that uses a local database connection is fine.
  2. Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. Check out the sample pages provided at /artists/1, /venues/1, and /shows/1 for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate.
  3. Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.
  4. Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.
  5. Implement search, powering the `/search` endpoints that serve the application's search functionalities.
  6. Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.


Acceptance Criteria
-----

1. The web app should be successfully connected to a PostgreSQL database. A local connection to a database on your local computer is fine.
2. There should be no use of mock data throughout the app. The data structure of the mock data per controller should be kept unmodified when satisfied by real data.
3. The application should behave just as before with mock data, but now uses real data from a real backend server, with real search functionality. For example:
  * when a user submits a new artist record, the user should be able to see it populate in /artists, as well as search for the artist by name and have the search return results.
  * I should be able to go to the URL `/artist/<artist-id>` to visit a particular artist’s page using a unique ID per artist, and see real data about that particular artist.
  * Venues should continue to be displayed in groups by city and state.
  * Search should be allowed to be partial string matching and case-insensitive.
  * Past shows versus Upcoming shows should be distinguished in Venue and Artist pages.
  * A user should be able to click on the venue for an upcoming show in the Artist's page, and on that Venue's page, see the same show in the Venue Page's upcoming shows section.
4. As a fellow developer on this application, I should be able to run `flask db migrate`, and have my local database (once set up and created) be populated with the right tables to run this application and have it interact with my local postgres server, serving the application's needs completely with real data I can seed my local database with.
  * The models should be completed (see TODOs in the `Models` section of `app.py`) and model the objects used throughout Fyyur.
  * The right _type_ of relationship and parent-child dynamics between models should be accurately identified and fit the needs of this particular application.
  * The relationship between the models should be accurately configured, and referential integrity amongst the models should be preserved.
  * `flask db migrate` should work, and populate my local postgres database with properly configured tables for this application's objects, including proper columns, column data types, constraints, defaults, and relationships that completely satisfy the needs of this application. The proper type of relationship between venues, artists, and shows should be configured.

## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/udacity/FSND.git
cd FSND/projects/01_fyyur/starter_code 
```

2. **Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:**
```
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```
Once you have finished editing your code, you can push the local repository to your Github account using the following commands.
```
git add . --all   
git commit -m "your comment"
git push -u origin master
```

3. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```

5. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## Infosources used during the development:


*Basic Relationship Patterns*¶ https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many



*Cross Site Request Forgery protection* [Cross Site Request Forgery protection | Django documentation | Django](https://docs.djangoproject.com/en/3.1/ref/csrf/)

*API to Jinja* [API — Jinja Documentation (2.11.x)](https://jinja.palletsprojects.com/en/2.11.x/api/#custom-filters)

*Babel Date and Time* [Date and Time — Babel 2.7.0 documentation](http://babel.pocoo.org/en/latest/dates.html#pattern-syntax)

*Frontend formats genres incorrectly. Is this supposed to happen? How do I take care of it?* [Knowledge - Udacity](https://knowledge.udacity.com/questions/188987)

*can ‘facebook_link’ be empty?* [Knowledge - Udacity](https://knowledge.udacity.com/questions/330487)

*Target database is not up to date* [python - Target database is not up to date - Stack Overflow](https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date)

*Flask init-db no such command* [python - Flask init-db no such command - Stack Overflow](https://stackoverflow.com/questions/58389621/flask-init-db-no-such-command)

*Flask - Bad Request The browser (or proxy) sent a request that this server could not understand [duplicate]* [python - Flask - Bad Request The browser (or proxy) sent a request that this server could not understand - Stack Overflow](https://stackoverflow.com/questions/48780324/flask-bad-request-the-browser-or-proxy-sent-a-request-that-this-server-could/48781606)

*How I Use Python Debugger to Fix Code* https://codeburst.io/how-i-use-python-debugger-to-fix-code-279f11f75866

*CSRF Flask* [Security Considerations — Flask Documentation (2.0.x)](https://flask.palletsprojects.com/en/master/security/#set-cookie-options)
[CSRF is (really) dead](https://scotthelme.co.uk/csrf-is-really-dead/)

*babel\dates.py AttributeError: ‘NoneType’ object has no attribute ‘days’* [Knowledge - Udacity](https://knowledge.udacity.com/questions/70223)

*genres not displayed correctly for venues* [Knowledge - Udacity](https://knowledge.udacity.com/questions/302981)

*ordering /venues and /shows page* [Knowledge - Udacity](https://knowledge.udacity.com/questions/262190)

*Edit and Update functions needed for Fyyur Project? (Nov 2020)* [Knowledge - Udacity](https://knowledge.udacity.com/questions/383199)

*Genres in venue/id route are kinds of messy* [Knowledge - Udacity](https://knowledge.udacity.com/questions/196162)

*IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM Todo* [Knowledge - Udacity](https://knowledge.udacity.com/questions/171591)

*Frontend formats genres incorrectly. Is this supposed to happen? How do I take care of it?* [Knowledge - Udacity](https://knowledge.udacity.com/questions/188987)

Other:

[Defining Constraints and Indexes —    SQLAlchemy 1.4 Documentation](https://docs.sqlalchemy.org/en/14/core/constraints.html)

[The Flask Mega-Tutorial Part III: Web Forms](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms) 
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

[pip freeze - pip documentation v20.3.3](https://pip.pypa.io/en/stable/reference/pip_freeze/)

[Primer on Python Decorators – Real Python](https://realpython.com/primer-on-python-decorators/#decorators-with-arguments)

[HTML Forms](https://www.w3schools.com/html/html_forms.asp)

[python - Form validation fails due missing CSRF - Stack Overflow](https://stackoverflow.com/questions/21501058/form-validation-fails-due-missing-csrf)

https://www.reddit.com/r/flask/comments/c5boap/flask_wtforms_csrf_token_missing_with/

[php - Cannot simply use PostgreSQL table name (“relation does not exist”) - Stack Overflow](https://stackoverflow.com/questions/695289/cannot-simply-use-postgresql-table-name-relation-does-not-exist)

[How can I drop all the tables in a PostgreSQL database? - Stack Overflow](https://stackoverflow.com/questions/3327312/how-can-i-drop-all-the-tables-in-a-postgresql-database)

[python - “module ‘babel’ has no attribute ‘dates’” when trying to format time and date - Stack Overflow](https://stackoverflow.com/questions/65611511/module-babel-has-no-attribute-dates-when-trying-to-format-time-and-date)

[string - Python How to get 1st element of date token - Stack Overflow](https://stackoverflow.com/questions/24174596/python-how-to-get-1st-element-of-date-token)

[python - How do I format a date in Jinja2? - Stack Overflow](https://stackoverflow.com/questions/4830535/how-do-i-format-a-date-in-jinja2)

[python - db.Model vs db.Table in Flask-SQLAlchemy - Stack Overflow](https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy)

[Flask-SQLAlchemy — Flask-SQLAlchemy Documentation (2.x)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

[Welcome to Flask — Flask Documentation (1.1.x)](https://flask.palletsprojects.com/en/1.1.x/)

## Result / Screenshots:

![alt text](https://github.com/ozieblo-repository/FSND/blob/master/projects/01_fyyur/starter_code/Screenshot%202021-01-23%20at%2000.00.16.png?raw=true)

![alt text](https://github.com/ozieblo-repository/FSND/blob/master/projects/01_fyyur/starter_code/Screenshot%202021-01-23%20at%2000.00.40.png?raw=true)
