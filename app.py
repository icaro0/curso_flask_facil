#imports
from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

#declaramos nuestra app
app = Flask(__name__)

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

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/create-data')
def createdata():
    admin = User('admin', 'admin@example.com', 'admin', True)

    post = Post('Title of a longer featured blog post', 'Multiple lines of text that form the lede, informing new readers quickly and efficiently about what’s most interesting in this post’s contents.', 'Multiple lines of text that form the lede, informing new readers quickly and efficiently about what’s most interesting in this post’s contents.', is_featured = True, featured_order=0)
    post1 = Post('Featured post', 'This is a wider card with supporting text below as a natural lead-in to additional content.', 'This is a wider card with supporting text below as a natural lead-in to additional content.', is_featured = True, featured_order=1)
    post2 = Post('Post title', 'This is a wider card with supporting text below as a natural lead-in to additional content.', 'Multiple lines of text that form the lede, informing new readers quickly and efficiently about what’s most interesting in this post’s contents.', is_featured = True, featured_order=2)

    #resto de posts
    post3 = Post('Sample blog post', 'This blog post shows a few different types of content that’s supported and styled with Bootstrap. Basic typography, images, and code are all supported.', '''<p>Yeah, she dances to her own beat. Oh, no. You could've been the greatest. 'Cause, baby, <a href="#">you're a firework</a>. Maybe a reason why all the doors are closed. Open up your heart and just let it begin. So très chic, yeah, she's a classic.</p>
        <blockquote>
          <p>Bikinis, zucchinis, Martinis, no weenies. I know there will be sacrifice but that's the price. <strong>This is how we do it</strong>. I'm not sticking around to watch you go down. You think you're so rock and roll, but you're really just a joke. I know one spark will shock the world, yeah yeah. Can't replace you with a million rings.</p>
        </blockquote>
        <p>Trying to connect the dots, don't know what to tell my boss. Before you met me I was alright but things were kinda heavy. You just gotta ignite the light and let it shine. Glitter all over the room <em>pink flamingos</em> in the pool. </p>
        <h2>Heading</h2>
        <p>Suiting up for my crowning battle. If you only knew what the future holds. Bring the beat back. Peach-pink lips, yeah, everybody stares.</p>
        <h3>Sub-heading</h3>
        <p>You give a hundred reasons why, and you say you're really gonna try. Straight stuntin' yeah we do it like that. Calling out my name. ‘Cause I, I’m capable of anything.</p>
        <pre><code>Example code block</code></pre>
        <p>Before you met me I was alright but things were kinda heavy. You just gotta ignite the light and let it shine.</p>
        <h3>Sub-heading</h3>
        <p>You got the finest architecture. Passport stamps, she's cosmopolitan. Fine, fresh, fierce, we got it on lock. Never planned that one day I'd be losing you. She eats your heart out.</p>
        <ul>
          <li>Got a motel and built a fort out of sheets.</li>
          <li>Your kiss is cosmic, every move is magic.</li>
          <li>Suiting up for my crowning battle.</li>
        </ul>
        <p>Takes you miles high, so high, 'cause she’s got that one international smile.</p>
        <ol>
          <li>Scared to rock the boat and make a mess.</li>
          <li>I could have rewrite your addiction.</li>
          <li>I know you get me so I let my walls come down.</li>
        </ol>
        <p>After a hurricane comes a rainbow.</p>''')
    post4 = Post('Another blog post', 'Lorem ipsum dolor sit amet', '''<p>I am ready for the road less traveled. Already <a href="#">brushing off the dust</a>. Yeah, you're lucky if you're on her plane. I used to bite my tongue and hold my breath. Uh, She’s a beast. I call her Karma (come back). Black ray-bans, you know she's with the band. I can't sleep let's run away and don't ever look back, don't ever look back.</p>
        <blockquote>
          <p>Growing fast into a <strong>bolt of lightning</strong>. Be careful Try not to lead her on</p>
        </blockquote>
        <p>I'm intrigued, for a peek, heard it's fascinating. Oh oh! Wanna be a victim ready for abduction. She's got that international smile, oh yeah, she's got that one international smile. Do you ever feel, feel so paper thin. I’m gon’ put her in a coma. Sun-kissed skin so hot we'll melt your popsicle.</p>
        <p>This is transcendental, on another level, boy, you're my lucky star.</p>''')
    post5 = Post('New feature', 'Lorem ipsum dolor sit amet', '''<p>From Tokyo to Mexico, to Rio. Yeah, you take me to utopia. I'm walking on air. We'd make out in your Mustang to Radiohead. I mean the ones, I mean like she's the one. Sun-kissed skin so hot we'll melt your popsicle. Slow cooking pancakes for my boy, still up, still fresh as a Daisy.</p>
        <ul>
          <li>I hope you got a healthy appetite.</li>
          <li>You're never gonna be unsatisfied.</li>
          <li>Got a motel and built a fort out of sheets.</li>
        </ul>
        <p>Don't need apologies. Boy, you're an alien your touch so foreign, it's <em>supernatural</em>, extraterrestrial. Talk about our future like we had a clue. I can feel a phoenix inside of me.</p>''')

    admin.save()

    users = User.query.all()
    post.user_id = users[0].id
    post1.user_id = users[0].id
    post2.user_id = users[0].id
    post3.user_id = users[0].id
    post4.user_id = users[0].id
    post5.user_id = users[0].id
    post.save()
    post1.save()
    post2.save()
    post3.save()
    post4.save()
    post5.save()
    return 'Datos insertados en BBDD'

@app.route('/admin')
def admin():
  posts = Post.get_all()
  return render_template('admin.html', posts = posts)

@app.route('/create-post-form')
def createPostForm():
  return render_template('create-post.html')

@app.route('/create-post', methods=['POST','GET'])
def createPost():
  if request.method == 'POST':
    post = Post(request.form['titulo'], request.form['resumen'], request.form['texto'])
    #set author from current 
    users = User.query.all()
    post.user_id = users[0].id
    post.save()
  return 'Post saved'
