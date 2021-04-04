#imports
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from urllib.parse import urlparse, urljoin


#declaramos nuestra app
app = Flask(__name__)
app.secret_key = "6Rfrl1kTpwl85St542WcAy97DZK4771N"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://argonautadigital:argonautadigital@localhost/argodigital'
db = SQLAlchemy(app)
from models import Post, User

db.create_all()
db.session.commit()


@app.route('/')
def index():
    featured_posts = db.session.execute(select(Post).where(Post.is_featured==True).order_by(Post.featured_order))
    posts = db.session.execute(select(Post).where(Post.is_featured==False).order_by(Post.publish_date.desc()))
    return render_template('index.html', featured_posts = featured_posts.scalars().all(), posts = posts.scalars().all())

@app.route('/post/<slug>')
def post(slug):
  post = Post.get_by_slug(slug)
  return render_template('post.html', post = post)


@app.route('/admin')
@login_required
def admin():
  posts = Post.get_all()
  return render_template('admin.html', posts = posts)

@app.route('/create-post', methods=['POST','GET'])
@login_required
def createPost():
  if request.method == 'POST':
    post = Post(request.form['titulo'], request.form['resumen'], request.form['texto'])
    #set author from current 
    if current_user.is_authenticated:
      post.user_id = current_user.id
      post.save()
    return redirect(url_for('admin'))
  return render_template('create-post.html')

@app.route('/edit-post/<id>', methods=['POST','GET'])
@login_required
def editPost(id):
  post = Post.get_by_id(id)
  if request.method == 'POST':
    post.title = request.form['titulo']
    post.summary = request.form['resumen']
    post.content = request.form['texto']
    #set author from current 
    if current_user.is_authenticated:
      post.user_id = current_user.id
      post.save()
  return render_template('edit-post.html', post=post)

@app.route('/delete-post/<id>', methods=['GET'])
@login_required
def deletePost(id):
  post = Post.get_by_id(id)
  post.delete()
  return redirect(url_for('admin'))

#Auth
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method =='POST':
    user = User.get_by_mail(request.form['email'])
    # Login and validate the user.
    if user is not None and user.check_password(request.form['password']):
      # user should be an instance of your `User` class
      login_user(user)
      flash('Logged in successfully.')
      next = request.args.get('next')
      if not is_safe_url(next):
        return abort(400)
      return redirect(next or url_for('index'))
    else:
      flash('Usuario invalido.')
  return render_template('login.html')

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and \
    ref_url.netloc == test_url.netloc


