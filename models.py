from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash,check_password_hash
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from app import db
import datetime
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __init__(self, name, email, password, is_admin):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_mail(email):
        return User.query.filter_by(email=email).first()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), nullable=False)
    publish_date = db.Column(db.DateTime())
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    featured_order = db.Column(db.Integer)

    def __init__(self, title, summary, content, is_featured=False, featured_order=0):
        self.title = title
        self.title_slug = slugify(title)
        self.summary = summary
        self.content = content
        self.publish_date = datetime.datetime.now()
        self.is_featured = is_featured
        self.featured_order = featured_order

    def __repr__(self):
        return f'<Post {self.title}>'
    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved= True
            except IntegrityError:
                count +=1
                self.title_slug = f'{slugify(self.title)}-{count}'
    def public_url(self):
        return url_for('post', slug = self.title_slug)
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug= slug).first()
    @staticmethod
    def get_by_id(id):
        return Post.query.filter_by(id= id).first()
    
    @staticmethod
    def get_all():
        return Post.query.all()

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime())
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    email = db.Column(db.String(256), nullable=False)
    def __init__(self, email, summary, content):
        self.email = email
        self.summary = summary
        self.content = content
        self.create_date = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
