from flask_login import UserMixin
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager


class BaseModel():
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone_number = db.Column(db.Integer(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    user_image = db.Column(db.String(), nullable=False, default="default.jpg")
    gender = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="User")

    def __init__(self, firstname, lastname, email, phone_number, password, gender, country, role="User"):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone_number = phone_number
        self.password = generate_password_hash(password)
        self.gender = gender
        self.country = country
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model, BaseModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    product = db.relationship('Product', backref=db.backref('comments', lazy=True), cascade="all, delete")


class Product(db.Model, BaseModel):
    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=False, default="default.jpg")
    quantity = db.Column(db.Integer(), nullable=False)
    brand = db.Column(db.String(), nullable=False)
    material = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    def __init__(self, name, price, description, image_url, quantity, brand, material, category):
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url
        self.quantity = quantity
        self.brand = brand
        self.material = material
        self.category = category

class Wishlist(db.Model, BaseModel):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlists', lazy=True))

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id


class Cart(db.Model, BaseModel):
    __tablename__ = "carts"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer(), default=1, nullable=False)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('carts', lazy=True))

    def __init__(self, user_id, product_id, quantity=1):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity


class GiftCard(db.Model, BaseModel):
    __tablename__ = 'gift_cards'

    id = db.Column(Integer, primary_key=True)
    amount = db.Column(db.Float)
    message = db.Column(db.String(500))
    code = db.Column(db.String(8), unique=True, nullable=False)
    is_sent = db.Column(db.Boolean, default=False)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    recipient_user_id = db.Column(Integer, ForeignKey('users.id'))
    sender = relationship('User', foreign_keys=[user_id])
    recipient = relationship('User', foreign_keys=[recipient_user_id], backref='received_gift_cards')


class Testimonial(db.Model, BaseModel):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)

    user = db.relationship('User', backref=db.backref('testimonials', lazy=True))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)