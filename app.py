#import Flask dependency
from flask import Flask
#We will add a new Flask app instance
app=Flask(__name__)
#We define the starting point or root
@app.route('/')
#The '/'  denotes that we want to put our data at the root of out routes. The forward slah is commonly known as the highest level of hierearchy in any computer system
def hello_world():
    return 'Hello world'
# This is an enviroment variable, these are essentially dynamic variables in the computer.
# These are used to modify the way a certain aspect of th computer operates
    

