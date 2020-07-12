# Cs50-Wiki
* item1 (0)
* item2 (0)
* item3 (0)
----
  * item1 (2)
    * item2 (4)
      * item3 (6)
-----
* item1 (0)
  * item2 (2)
    * item3 (4)
-----
   * item1 (3)
     * item2 (5)
       * item3 (10) *maximum 5 min:2* 

nested li is defined in such a way that difference between new li and prev li must be diff>=2 and diff<=5
------------
* item1 (0)
     * item2 (2)
-----
     
7. Channel.js: **(Messages View,Sending Messages,Personal Touch)**
         
      * On DOMContentLoaded:
        * Disables send message button if message is empty. Send message button is active only if there is a message or any attachements.  
        * Establish Socket connection between server and client.
        * Send message: 
           * Socket emit with user message , date, time and attachments (if any) to server. 
        * Announce message: 
           * Socket announce to client
             * Stores current channel in local storage **(For Remembering Channel Feature)**
             * Creates new divs for the new messages .
             * Creates new divs to support delete message feature
        * Display error message if user try to delete or send message to a channel which is not yet created.

  8. main.css:

      * CSS Styling for entire application.

  9.requirements.txt:

      * Information about the Python packages that are used by the application.
           
         
### Built with:
--------------------

  1. [Bootstrap (version: 4.5)](https://getbootstrap.com/)

  2. [Microsoft Visual code (version:1.44)](https://code.visualstudio.com/)

  3. [Flask (version: 1.1.2)](https://flask.palletsprojects.com/en/1.1.x/)

  4. [Flask-Session(version: 0.3.2)](https://flask.palletsprojects.com/en/1.1.x/)
  
  5. [Flask-SocketIO(version: 4.3.0)](https://flask-socketio.readthedocs.io/en/latest/)
  
  6. [Jinja2 (version: 2.11.2)](https://jinja.palletsprojects.com/en/2.11.x/)
  
  7. [Python(version 3.7.3)](https://www.python.org/)
  
  8. HTML5
  
  9. Javascript ES6
  
  10. Cascading Style Sheets (CSS)
  
### Author:
------------
NAIR SAARIKA BHASI
# saarikabhasi
