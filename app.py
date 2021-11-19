#Adding flask dependency 
from flask import Flask

#Creating a new flask app instance
#Instance is the general term for refering to a singular version of something
app = Flask(__name__)
#__name__ 


#This "@app.route('/')" is the starting point or the root of the route
#the '/' indicates the highest level of hierarchy in any computer system directory
@app.route('/')
def hello_world():
    return 'Hello world! :D'
    