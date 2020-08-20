# CS50 Web Programming with Python and JavaScript

Webpage link: https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/

# Project 2: Flack

### Description:

Development of chat application - **'Flack'** 

The Flack application allows its user to communicate with each other through channels. 

#### Features:
  
  * Create a new channel
  * Join existing channel
  * See previous messages (upto 100 messages)
  * Shows each message's message, time, date and attachments (if any).
  
    **Personal touch:**
  
    
  * Search for a channel. Display channnel names if a match is found, else display 'no results' or 'no channels found'
  * Send attachments : Accepts Image (jpg) and Document(doc,docx,pdf)
  * Delete old and new message ( *note: User can delete only their message* )
  * Show if the message was deleted. 
    * Note: 
      * Shows "This message was deleted" for other user's deleted message
      * Shows "You have deleted this message" for current user's deleted message 

  ### File Specific and Feature details:

  1. application.py: 

       * Server side program, in Python and Flask.
       * Handles socket transactions using flask_socketio
       * Stores channel's chat messages in a dictionary. 
          * If channel messages exceeds 100 messages, does a popleft of oldest message for that channel  until the dictionary has maximum of 100 messages. 
       * Chat application routing, error handling and user session information .

  #### File path: templates/:
    
   
  2. login.html:**(Display Name)** 
     
        * Gets user display name
          * Error message is thrown if, display name is empty. 
        * Stores display name in local storage and in flask session.
        
  3. index.html: **(Channel Creation,Channel List)**
     
        * Displaying all channels ( hyperlink to channel page )
        
        * Create channel ( displayed in a modal )
          * A new channel is created only if the new channel name does not already exists.
          
        * Search for existing channels
          * Shows result if found a match ( hyperlink to channel page )
          
        * Javascript code : 
          * Setting background color of body
          * Display create channel modal again, if channel name already exists.
          
  
          
          * **(Remembering Channel)** If the user was communicating on a channel and closes the window, and when the user open the application again, it displays previous channel the user was on.
            
  4. channel.html: **(Messages View,Sending Messages,Personal Touch)**
     
        * Display selected channel information and previous messages ( shows upto 100 messages )
        * Displays message on right if send by current user and left if send by other users
        * Show each message's display name, time, date and attachments.
        * Write message input box where user can type message, attach image and/or document and a send message button.
        * Show delete message button for all previous and new messages. 
          * Note: User can delete only their message
    
        
  5. layout.html:
     
        * Base layout for all the above html files.
        
        * Navigation bar
          * Logo
          * All channnels (redirects to index.html and shows all channels)
          * Shows current user's display name
          * Logout button
        
        * Javascript code : 
          * When user clicks logout button, clears all the information stored in local storage
          
          **(For Remembering Channel Feature)**
          * When user clicks all channels button it resets current channel information stored in local storage.
          
   #### File path: static/: 
   
  6. login.js:**(Display Name)** 
      
         * Set background color for body
         
         * Checks in local storage for display name
            * if already set, then redirects to server with previous display name. 
            * if not already set, then gets display name from user.
            
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

  9. requirements.txt:

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