# CS50 Web Programming with Python and JavaScript

Webpage link: https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/


## Project 1: Books

Webpage link: https://the-booklover.herokuapp.com/

<p> 
  
  <img src="https://user-images.githubusercontent.com/55930906/84531715-fbfc6600-acb2-11ea-8a17-911be2c38297.png?raw=true"  width =450 height =450 alt= "Login">
  
  
  <img src="https://user-images.githubusercontent.com/55930906/84535544-feae8980-acb9-11ea-81e3-a508bcdd6e33.png?raw=true"  width =450 height =450 alt= "Search">
    <img src="https://user-images.githubusercontent.com/55930906/84529435-732ffb00-acaf-11ea-98b7-a375865f4b8c.png?raw=true"   width =450 height =450 alt= "book">
       <img src="https://user-images.githubusercontent.com/55930906/84529458-7aef9f80-acaf-11ea-8c5c-8bbbe29e1cb1.png?raw=true"   width =450 height =450 alt= "book">
        <img src="https://user-images.githubusercontent.com/55930906/84529464-7d51f980-acaf-11ea-941a-9fe718b06a3c.png?raw=true"  width =450 height =450  alt= "author">
        <img src="https://user-images.githubusercontent.com/55930906/84529470-804cea00-acaf-11ea-803a-0341d39dd645.png?raw=true"  width =450 height =450  alt ="myreview">
        
 </p>     
      
      
    

### Description:

Development of a Book Reviewing website - **'The Book Fair'** 

The Book Fair website allows its user to register, search for a book, see the book details, and leave comments and rate the book on the scale of 1 to 5 . It also displays the Book's average rating and comments left by other readers in the Book Fair website and pulls Rating information from third-party website such as **Good Reads and Google Books**.  


### General information:

1. Pulls book publisher details, description, book cover thumbnail image  from the Google books API.
2. Database setup using Heroku and PostgreSQL.
3. Supports smaller screens.
4. Users can make a API get request to the website by https://the-booklover.herokuapp.com/api/isbn.
   * isbn is the book isbn number:
       * Example:
            * https://the-booklover.herokuapp.com/api/0380753022 (isbn: 0380753022)
            
              ```
              {
                "author":"Johanna Lindsey",
                "average_score":2.67,
                "isbn":"0380753022",
                "review_count":4,
                "title":"Gentle Rogue",
                "year":1990
                }
              ```
              
            * 404 error if isbn in not found in the DB:
              ```
              {
              "error":"Invalid isbn number",
              "status_code":404
              }
              ```


### Setup:
---------------
  ``` 
    # clone repository
      git clone https://github.com/saarikabhasi/CS50-project1-Books.git
      
    # Create a virtualenv(optional)
      python3 -m venv venv  
      
    # Activate the virtualenv
      source venv/bin/activate or .venv/bin/activate
      
    # Install all dependencies
       pip install -r requirements.txt
       
    # ENV Variables
        export FLASK_APP=application.py 
        export FLASK_ENV=development  #To enable debug mode. Reference#https://flask.palletsprojects.com/en/1.1.x/config/
        export DATABASE_URL = Heroku Postgres DB URI 
        export GR_key = Goodreads API Key. Reference#https://www.goodreads.com/api/keys 
   ```
        
 ### Database Schema:
 --------------------
 1) Books( book_id	integer, isbn	varchar, title	varchar, author	varchar, year	integer)  
    * Primary key:
       * isbn
    
 2) users(user_id	integer,email_id	varchar, password	varchar,name	varchar)
    * Primary key: 
       * email_id
     
 3) reviews(id	integer,	contents	text NULL	, rating	numeric NULL, isbn	varchar, email_id	varchar)
    * Primary key: 
      * id
    * Foreign Key: 
        * isbn refers to (books:isbn)
        * email_id refers to (users:email_id)	
        
### Built with:
--------------------

1. [Bootstrap (version: 4.5)](https://getbootstrap.com/)

2. [Microsoft Visual code (version:1.44)](https://code.visualstudio.com/)

3. [Flask (version: 1.1.2)](https://flask.palletsprojects.com/en/1.1.x/)

4. [Flask-Session(version: 0.3.2)](https://flask.palletsprojects.com/en/1.1.x/)

5. [gunicorn (version: 20.0.4)](https://pypi.org/project/gunicorn/)

6. [Jinja2 (version: 2.11.2)](https://jinja.palletsprojects.com/en/2.11.x/)

7. [psycopg2 (version: 2.8.5)](https://pypi.org/project/psycopg2/)

8. [requests (version: 2.23.0)](https://pypi.org/project/requests/)

9. [SQLAlchemy(version:1.3.17)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

10. [Werkzeug(version:1.0.1)](https://werkzeug.palletsprojects.com/en/1.0.x/)

11. [Python(version 3.7.3)](https://www.python.org/)

12. HTML5

13. Cascading Style Sheets (CSS)



### Author:
------------
NAIR SAARIKA BHASI