# Item Catalog
Lists items within a variety of sports categories and provides registration and authentication via Google. Registered users can post, edit and delete their own items. Bootstrap is used for front-end and user interface components.

#Usage
Run application.py. 
The catalog already includes sample data. Google sign-in is required to create/edit/delete items.
JSON endpoints can be accessed in the menu under "Export". Endpoint for category items is available only when viewing a category.

##database_setup.py
Defines the database tables and relationships. Creates classes for use with SQLAlchemy.

##gen_items.py
Creates sample categories and items. Default user (creator) is 'Han Solo'.

##application.py
Runs the item catalog application: HTTP server, 
