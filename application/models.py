"""Database models."""
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import pandas as pd


df = pd.read_excel(r'application/excel_database/calo.xlsx') # Import products calories data from excel file

engine = create_engine('sqlite:///instance/test.db') # Connect to sql database
df.to_sql('food', con=engine, if_exists='replace', index=False) # Write data to database with table name 'products'


class Food(db.Model):
    """Food model."""

    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=False)
    cal = db.Column(db.Float, unique=False, nullable=False)

    def as_dict(self):
        return {'name': self.name}


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False, unique=False)
    username = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Log(db.Model):
    """User Log model."""

    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    date = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    gr = db.Column(db.Float,unique=False,nullable=False)

    # Relationship
    user = relationship('User')
    food = relationship('Food')

    @property
    def total(self):
        return self.food.id.cal * self.gr

    def __repr__(self):
        return '<Calendar {}>'.format(self.email)


class Feedback(db.Model):
    """Feedback model."""

    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    phone = db.Column(db.String(40), unique=False, nullable=False)
    body = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return '<Feedback {}>'.format(self.fullname)
