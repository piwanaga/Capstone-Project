from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Text, nullable=False, unique=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, default="/static/images/default-avatar.png")

    market = db.Column(db.Text, db.ForeignKey("markets.code", ondelete='CASCADE'), default="en-US")
    
    saved_articles = db.relationship('SavedArticle', backref='users', passive_deletes=True)

    pref_market = db.relationship('Market', backref='users', passive_deletes=True)


    @classmethod
    def signup(cls, email, username, password):
        """Sign up user. Hashes password and adds user to system"""
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with username, check password hash"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class SavedArticle(db.Model):
    """Articles that have been saved by users"""

    __tablename__ = "saved_articles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)

    url = db.Column(db.Text, primary_key=True)

    name = db.Column(db.Text, nullable=False)

class Market(db.Model):
    """Market codes for where Bing API results will come from"""

    __tablename__ = "markets"

    code = db.Column(db.Text, primary_key=True)

    name = db.Column(db.Text)

class Category(db.Model):
    """Categories for news articles returned by Bing API"""

    __tablename__ = "categories"

    name = db.Column(db.Text, primary_key=True)

    icon = db.Column(db.Text)

class MarketCategory(db.Model):
    """Abailable categories for each market"""

    __tablename__ = "market_categories"

    mkt_code = db.Column(db.Text, db.ForeignKey("markets.code", ondelete="CASCADE"), primary_key=True)

    cat_name = db.Column(db.Text, db.ForeignKey("categories.name", ondelete="CASCADE"), primary_key=True)

    categories = db.relationship("Category", backref="market_categories")

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)

STORIES = [ 
        {
            "name": "Sample Story 1",
            "url": "http://www.weather.com/",
            "description": "This is a sample story. La di da.",
            "image": {
                "thumbnail": {
                    "contentUrl": "https://pocket-image-cache.com/direct?resize=w2000&url=https%3A%2F%2Fichef.bbci.co.uk%2Fwwfeatures%2Flive%2F976_549%2Fimages%2Flive%2Fp0%2F5b%2Fq2%2Fp05bq2r8.jpg"
                }
            },
            "datePublished": "2020-11-10T22:05:00.0000000Z",
            "provider": [
                {"name": "Bloomberg"}
            ]
        },
        {
            "name": "Another Great Story",
            "url": "http://www.springboard.com/",
            "description": "Blah Blah Blah. This is a really good story",
            "image": {
                "thumbnail": {
                    "contentUrl": "https://pocket-image-cache.com/direct?resize=w2000&url=https%3A%2F%2Fichef.bbci.co.uk%2Fwwfeatures%2Flive%2F976_549%2Fimages%2Flive%2Fp0%2F5b%2Fq2%2Fp05bq2r8.jpg"
                }
            },
            "datePublished": "2020-11-10T22:05:00.0000000Z",
            "provider": [
                {"name": "The Washington Post"}
            ]
        },
        {
            "name": "Wahoo another story",
            "url": "http://www.weather.com/",
            "description": "This is a sample story. La di da.",
            "image": {
                "thumbnail": {
                    "contentUrl": "https://pocket-image-cache.com/direct?resize=w2000&url=https%3A%2F%2Fichef.bbci.co.uk%2Fwwfeatures%2Flive%2F976_549%2Fimages%2Flive%2Fp0%2F5b%2Fq2%2Fp05bq2r8.jpg"
                }
            },
            "datePublished": "2020-11-10T22:05:00.0000000Z",
            "provider": [
                {"name": "Bloomberg"}
            ]
        },
        {
            "name": "More Stories!",
            "url": "http://www.springboard.com/",
            "description": "Blah Blah Blah. This is a really good story",
            "image": {
                "thumbnail": {
                    "contentUrl": "https://pocket-image-cache.com/direct?resize=w2000&url=https%3A%2F%2Fichef.bbci.co.uk%2Fwwfeatures%2Flive%2F976_549%2Fimages%2Flive%2Fp0%2F5b%2Fq2%2Fp05bq2r8.jpg"
                }
            },
            "datePublished": "2020-11-10T22:05:00.0000000Z",
            "provider": [
                {"name": "The Washington Post"}
            ]
        }
    ]

TOPICS = [
    {
        "name": "Trending Topic",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "Election 2020",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "Dogs and Cats",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "Covid 19 Cases",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "Michigan, Pennsylvania, Nevada",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "China did something",
        "query":{
                "text":"McConnell stimulus bill"
                }
    },
    {
        "name": "Stocks and money and stuff",
        "query":{
                "text":"McConnell stimulus bill"
                }
    }
]