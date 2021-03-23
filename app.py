#imports
from flask import Flask
from flask import render_template

#declaramos nuestra app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post.html')