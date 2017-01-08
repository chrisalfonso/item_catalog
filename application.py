from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

from flask import session as login_session
import random, string

#For Google sign in
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']

def getUserID(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None

def getUserInfo(user_id):
	try:
		user = session.query(User).filter_by(id = user_id).one()
		return user
	except:
		return None

def createUser(login_session):
	newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] =  state
	#return "The current state is %s" % login_session['state']
	return render_template('login.html', STATE=state)

# JSON ENDPOINT: all items in category
@app.route('/catalog/<category_name>/item/JSON')
def categoryItemsJSON(category_name):
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id).all()
	return jsonify(CategoryItems=[b.serialize for b in items])

# JSON ENDPOINT: single item
@app.route('/catalog/<category_name>/item/<item_name>/JSON')
def categoryItemJSON(category_name, item_name):
	item = session.query(Item).filter_by(name = item_name).one()
	return jsonify(item = item.serialize)

# JSON ENDPOINT: all categories
@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [r.serialize for r in categories])

# PROFILE PAGE
@app.route('/profile')
def profile():
	categories = session.query(Category).order_by(asc(Category.name)) # to list all existing categories in menu
	
	if 'username' not in login_session:
    	return redirect('/login')
	else:  
    	return render_template('profile.html', name=login_session['username'], id=login_session['user_id'], pic=login_session['picture'], categories=categories) 
	"""
	Other items available:
	login_session['credentials']
	login_session['gplus_id']
	login_session['username']
	login_session['email']
	login_session['picture'] 
	"""


# HOMEPAGE
@app.route('/')
@app.route('/catalog/')
def showCategories():
	categories = session.query(Category).order_by(asc(Category.name))
	recent_items = session.query(Item).order_by(desc(Item.id)).join(Item.category).limit(6)

	return render_template('main_new.html', categories=categories, items=recent_items)


# CREATE a new CATEGORY
@app.route('/catalog/new/', methods=['GET','POST'])
def newCategory():
	categories = session.query(Category).order_by(asc(Category.name))

	if 'username' not in login_session:
		return redirect('/login')

	if request.method == 'POST':
		newCategory = Category(name = request.form['name'], user_id = login_session['user_id'])
		session.add(newCategory)
		session.commit()
		flash('New category "%s" successfully created' % newCategory.name)
		return redirect(url_for('showCategories'))
	else:
		return render_template('category_new_rev.html', categories=categories)


# EDIT a CATEGORY
@app.route('/catalog/<category_name>/edit/', methods = ['GET', 'POST'])
def editCategory(category_name):
	editedCategory = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = editedCategory.id).all() # added for new template
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template

	if 'username' not in login_session:
		return redirect('/login')

	if editedCategory.user_id != login_session['user_id']:
		flash('You are not authorized to edit this category. You must be the category owner.')
		return redirect(url_for('showItem', category_name=editedCategory.name))

	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
			session.add(editedCategory)
			session.commit()
			flash('Category updated')
			return redirect(url_for('showItem', category_name=editedCategory.name))
	else:
		return render_template('category_edit_rev.html', category=editedCategory, categories=categories, items=items)


# DELETE a CATEGORY
@app.route('/catalog/<category_name>/delete/', methods = ['GET','POST'])
def deleteCategory(category_name):
	categoryToDelete = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = categoryToDelete.id).all() # added for new template
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template
	
	if 'username' not in login_session:
		return redirect('/login')

	if categoryToDelete.user_id != login_session['user_id']:
		flash('You are not authorized to delete this category. You must be the category owner.')
		return redirect(url_for('showItem', category_name=categoryToDelete.name))

	if request.method == 'POST':
		session.delete(categoryToDelete)
		session.commit()
		flash('%s Successfully Deleted' % categoryToDelete.name)
		return redirect(url_for('showCategories'))
	else:
		return render_template('category_delete_rev.html', category=categoryToDelete, items=items, categories=categories)


# SHOW CATEGORY ITEMS
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name):
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template
	category = session.query(Category).filter_by(name = category_name).one()
	items = session.query(Item).filter_by(category_id = category.id).all()

	# User must be logged in to view category items
	if 'username' not in login_session:
		return redirect('/login')
	else:
		return render_template('items_rev.html', items=items, category=category, categories=categories, creator=login_session['username'], pic=login_session['picture'])


# CREATE a new ITEM
@app.route('/catalog/<category_name>/item/new/',methods=['GET','POST'])
def newItem(category_name):
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template
	category = session.query(Category).filter_by(name=category_name).one()

	# Redirect if user is not logged in
	if 'username' not in login_session:
		return redirect('/login')

	# Prevent users from accessing 'create item' form directly by URL
	if category.user_id != login_session['user_id']:
		flash('You are not authorized to create new menu items for %s. You must be the creator of the category.' % category.name)
		return redirect(url_for('showItem', category_name=category.name))

	if request.method == 'POST':
		newItem = Item(name = request.form['name'], description = request.form['description'], category_id = category.id, user_id = login_session['user_id'])
		session.add(newItem)
		session.commit()
		flash('New item "%s" was successfully created' % (newItem.name))
		return redirect(url_for('showItem', category_name=category.name))
	else:
		return render_template('item_new_rev.html', category=category, categories=categories)


# EDIT an ITEM
@app.route('/catalog/<category_name>/item/<item_name>/edit', methods=['GET','POST'])
def editItem(category_name, item_name):
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template
	category = session.query(Category).filter_by(name = category_name).one()
	editedItem = session.query(Item).filter_by(name = item_name).one()

	# User must be logged in to edit items
	if 'username' not in login_session:
		return redirect('/login')

	# Users can only modify items they themselves have created
	if editedItem.user_id != login_session['user_id']:
		flash('You are not authorized to edit this item. You must be the creator of this category.')
		return redirect(url_for('showItem', category_name=category.name))

	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		session.add(editedItem)
		session.commit() 
		flash('Item updated')
		return redirect(url_for('showItem', category_name=category.name))  
	else:
		return render_template('item_edit_rev.html', category=category, item=editedItem, categories=categories)


# DELETE an ITEM
@app.route('/catalog/<category_name>/item/<item_name>/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(category_name,item_name,item_id):
	categories = session.query(Category).order_by(asc(Category.name)) # added for new template
	category = session.query(Category).filter_by(name = category_name).one()
	itemToDelete = session.query(Item).filter_by(id = item_id).one()

	# User must be logged in to delete items
	if 'username' not in login_session:
		return redirect('/login')

	# Users can only delete items they themselves have created
	if itemToDelete.user_id != login_session['user_id']:
		flash('You are not authorized to delete this item. You must be the creator of this category.')
		return redirect(url_for('showItem', category_name=category.name))

	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('%s successfully deleted' % itemToDelete.name)
		return redirect(url_for('showItem', category_name=category.name))
	else:
		return render_template('item_delete_rev.html', item=itemToDelete, category=category, categories=categories)
  

# Google authentication
@app.route('/gconnect', methods=['POST'])
def gconnect():
	#Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Obtain authorization code
	code = request.data
	
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Ensure access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	# If there's an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 50)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		reponse = make_response(json.dumps("Token's client ID does not match app ID", 401))
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check to see if user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'

	# Store the access token in the session for later use
	login_session['credentials'] = credentials.access_token # added '.access_token' due to non serializable error
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	# CREATE USER if one doesn't already exist
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
		login_session['user_id'] = user_id 

	output = ''
	output += '<h3>Welcome, '
	output += login_session['username']
	output += '!</h3>'
	output += '<img src="'
	output += login_session['picture']
	output += '" style="width: 150px; height: 150px; border-radius: 150px; -webkit-border-radius: 150px;-moz-border-radius: 150px;">'
	flash("You are now logged in as %s" % login_session['username'])
	print "done!"
	return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Execute HTTP GET request to revoke current token.
	access_token = login_session.get('credentials') #credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# Reset the user's session.
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	else:
		# For whatever reason, the given token was invalid
		response = make_response(json.dumps('Failed to revoke token for given user'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
