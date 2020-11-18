import os
from unittest import TestCase

from models import db, User, SavedArticle, Market, Category, MarketCategory

os.environ['DATABASE_URL'] = "postgresql:///currant-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test User model"""

    @classmethod
    def setUpClass(cls):
        """Add test market to db"""
        Market.query.delete()

        m = Market(code="en-US", name="United States")

        db.session.add(m)
        db.session.commit()
        
    def setUp(self):
        """Create test client and delete any existing data from tables"""

        User.query.delete()
        SavedArticle.query.delete()

    def test_user_model(self):
        """Test basic User model and relationships"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http://www.picture.com", 
            market="en-US"
        )

        db.session.add(u)
        db.session.commit()

        self.assertIsNotNone(User.query.get(u.id))
        self.assertEqual(len(u.saved_articles), 0)
        self.assertEqual(u.pref_market.name, "United States")

    def test_signup(self):
        """Test User signup method"""

        u = User.signup("test@test.com", "testuser", "password")

        db.session.commit()

        self.assertIsNotNone(User.query.get(u.id))
        self.assertEqual(len(u.saved_articles), 0)
        self.assertEqual(u.email, "test@test.com")

    def test_authenticate(self):
        """Test User authenticate method"""

        u = User.signup("test@test.com", "testuser", "password")

        db.session.commit()

        self.assertIsNot(User.authenticate("testuser", "password"), False)
        self.assertIsInstance(User.authenticate("testuser", "password"), User)

    def test_saved_articles(self):
        """Test adding a saved article in the db"""

        u = User.signup("test@test.com", "testuser", "password")

        db.session.commit()

        article = SavedArticle(user_id=u.id, url="www.test.com", name="test article")
        
        db.session.add(article)
        db.session.commit()

        self.assertEqual(len(u.saved_articles), 1)
        self.assertEqual(u.saved_articles[0].name, "test article")
        self.assertEqual(u.saved_articles[0].url, "www.test.com")