from app import db
from flask_login import UserMixin
from datetime import datetime



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique = True, nullable = False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<User {self.username} ({self.email})>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  
    

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)

    product = db.relationship('Product', backref=db.backref('images', lazy=True, cascade='all, delete-orphan'))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey('category.id', name='fk_category_id', ondelete='CASCADE'),
        nullable=False
    )
    user = db.relationship('User', backref='products')
    category = db.relationship('Category', backref='products', lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"
    
    @property
    def first_image(self):
        if self.images:
            return self.images[0].url
        return None 


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_cart_user_id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', name='fk_cart_product_id', ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    product = db.relationship('Product', backref='cart_items', lazy='joined')
    user = db.relationship('User', backref='cart_items')

    
class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_user_id", ondelete='CASCADE'), nullable=False)
    details = db.Column(db.JSON, nullable=False)
    checkout_time = db.Column(db.DateTime, default=datetime.now())
    total_price = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    buyer = db.relationship('User', backref='checkouts')