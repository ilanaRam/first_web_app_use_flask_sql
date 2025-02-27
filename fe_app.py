from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os


# -----------------------------------------------------------
# Based on Video: https://www.youtube.com/watch?v=qbLc5a9jdXo
# -----------------------------------------------------------

# this app uses package Flask to make web application
# To run it from terminal (pyCharm terminal, we use this cmd:
# python -m flask --app fe_app run
# if app running well we will see this output on the terminal: "Running on http://127.0.0.1:5000

# Question: Why do we see this ip address?
# Answer: This ip address comes from Flask’s built-in development server.
# Flask automatically starts its built-in web server. The default behavior is:
#
# Host: 127.0.0.1 → This means the app is running on localhost, which is only accessible from your own machine.
# Port: 5000 → This is the default port Flask chooses unless you specify another one.
# This behavior is hardcoded in Flask unless you explicitly change it

# Question: what happens when we hit the ip address?
# answer: is sent REST API - GET with URL: URL is built from:
# Usually URL consist of the next 6 parts:

# 1. Protocol                                                              (http)
# 2. IP Address / Domain name                                              (127.0.0.1)
# 3. Port number                                                           (5000)
# 4. Path - specific location in the resource                              (/drinks)
# 5. Query                                                                 (GET)
# 6. Fragment (in case we wish to access specific section of the resource) (/id)

# Exp url is: http://127.0.0.1:5000/drinks/2  while the request type is: GET


# 1 Create db obj - of the type SQLAlchemy (no word about the app)
db = SQLAlchemy()

# 2 Create app (use Flask module)
app = Flask(__name__)

# 3 Here we connect between DB and the app
# Configure the app to work with SQLALCHEMY (app will use db called: drinks.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4 Initialize db with the app - this is actual binding between app and db
db.init_app(app)

# db_path is set with a location where will be created a db in the project
db_path = "instance/drinks.db"

# 5 create data base model - in simple words it creates a table of the type Drink, which name = class name but in lowercase
# class defines the class model of the table.
# DB is drinks.db but it will contain 1 table inside it, called drink
# because we use SQLAlchemy, SQLAlchemy automatically creates a table named drink in the database.
# if we use this attribute in the class Drink: __tablename__ = 'my_drinks'  # Set the table name explicitly to be 'my_drinks' instead of drink (table name = DB name)
class Drink(db.Model):
    # I set here the explicit name for the table that will be created in my DB
    # If we do not set the name explicitly, its default name will be as a class name, but in lover case (e.g: drink)
    __tablename__ = 'my_drinks'

    # here I define that in table 'drinks' will be 3 columns: id, name, description
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True,nullable=False)
    description = db.Column(db.String(80))

    # magic func of the class for object (self) representation
    def __repr__(self):
        return f"{self.name}-{self.description}"

# remove db from the project if it created previously
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old database deleted.")

# this is most importent place - here we define a context of the app, within the context of the app we reset the DB
with app.app_context():
    db.drop_all() # !!! Delete DB
    db.create_all()  # !!! Create empty DB file .db in project path: root/instance
    print(f"Running not in the main context, Created a new table: {Drink.__tablename__}")

# ----------------------------------------------------------
# Hitters / routes - kind of callback that will be called upon our hit (click / press)
# these are all operations that will be taken upon our click on / rout
# ----------------------------------------------------------

# this is a decorator in Flask, that determines a URL then binds URL with my function. Flask determines what URL triggers my function. Then the func is called.
# When I click (=visit) this URL (http://127.0.0.1:5000 as this is Flask default IP and URL) will be invoked function: index()
# in which I do: # I print 'Hello you'
@app.route('/')
def index():
    return 'Hello you !'

# When I click (=visit) this URL (http://127.0.0.1:5000/drinks, I write /drinks at the browser), Flask binds it to my function: get_drinks()
@app.route('/drinks')
def get_drinks():# we define a method we wish to hit when someone visits a route
    print('Reading all the drinks from the table !!')
    output = []

    all_drinks = Drink.query.all()
    if not all_drinks:
        print("DB is empty !!")
        return output

    print("Here are all the drinks that we could retrieve from the SB:")
    for drink in all_drinks:
        drink_data = {'id': drink.id,
                      'name': drink.name,
                      'description': drink.description}
        print(drink_data)
        output.append(drink_data)
    return output

# When I click (=visit) this URL (http://127.0.0.1:5000/drinks/2, I write /drinks/2 at the browser), Flask binds it to my function: get_drink_by_id(id)
@app.route('/drinks/<id>')
def get_drink_by_id(id):# we define a method we wish to hit when someone visits a route
    print('Trying to read a drink by id')
    drink = Drink.query.get_or_404(id)
    return ({"name": drink.name,
             "description": drink.description})

# !!! By default, route decorator of the Flask handles 'GET' requests. If you need POST, PUT, DELETE, you specify them as a param to the decorator route:
# When I click (=visit) this URL (http://127.0.0.1:5000/drinks, , Flask binds it to my function: add_drink(id)
# this one for posting the new resource = adding new drink to the data base
# I enter the details of the new resource (name, description) from the web browser and not hard codded here in the code !!
# 'request' brings the name and description from web to the code !! -> web client posts a new resource into the web server (my code here)
# the function add_drink() will be called when a user decided to make POST from URL http://127.0.0.1/drinks
# I can use Postman to send POSTS to my app
# I write in Postman the url: http://127.0.0.1/drinks
# in the body I write: (also I select *raw)
#
# {
#   "name": "Apple Juice",
#   "description": "Fresh apple juice"
# }
# I click on 'Send'
# request is sent to my app, Flask prepares the request and I can use in my app code the request object that holds deserialized data (that I need to convert into dict)
@app.route('/drinks', methods=['POST'])
def add_drink():# we define a method we wish to hit when someone visits a route
    print('Trying to post new drink ...')

    # get data from the POST request:
    # request is serialized object (means bits) in order to work with it we need to deserialize it into dict
    posted_drink_data_request = request.json

    print(f"User created a POST request with the next new data (new drink), "
          f"name:{posted_drink_data_request['name']}, description: {posted_drink_data_request['description']}")

    # build data base object based on posted data (based on the POST request)
    drink = Drink(name=posted_drink_data_request['name'],
                  description=posted_drink_data_request['description'])
    print(f"The drink obj is ready to pushed into db ...")

    db.session.add(drink)
    db.session.commit()
    print(f"New drink was added to the data base, the id: {drink.id}")
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):# we define a method we wish to hit when someone visits a route
    print(f"User created a DELETE request to delete the drink({id})")
    drink = Drink.query.get(id)
    if drink is None:
        print(f"Such drink item is not in the table ##")

    print(f"This drink item is in the table and will be deleted")
    db.session.delete(drink)
    db.session.commit()
    print(f"Drink: {drink}, was deleted from the table: {Drink.__tablename__}")
    return {"message":"YEEEE"}



# if __name__ == '__main__':
#
#     print(f"Application is running within a context of the main ...")
#     with app.app_context():
#         db.drop_all() # !!! Delete DB
#         db.create_all()  # !!! Create empty DB file .db in project path: root/instance
#         print(f"Table have been created: {Drink.__tablename__}")
#
#     # push hard codded few items into DB
#     print(f"Pushing hard codded few drink items into the table: {Drink.__tablename__}...")
#     drink = Drink(name="Grape Soda", description="sparkling water with grape taste")
#     print(drink)
#     db.session.add(drink)  # logical insert of the new resource (new data)
#     db.session.commit()  # actual insert
#
#     drink = Drink(name="Cola", description="Coka cola")
#     print(drink)
#     db.session.add(drink)
#     db.session.commit()
#
#     print(f"\nQuerying db to retrieve  (GET) all drink items back ...")
#     all_drinks = Drink.query.all()
#     for drink in all_drinks:
#         print(drink)
#
#     #app.run(debug=True) # This allows running the app directly = via main
