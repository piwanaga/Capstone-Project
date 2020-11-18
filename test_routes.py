import os
from unittest import TestCase

from models import db, connect_db, User, Market, SavedArticle

os.environ['DATABASE_URL'] = "postgresql:///currant-test"

from app import app, CURR_USER_KEY, URL, HEADERS

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ArticleRoutesTestCase(TestCase):
    """Test article routes"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Market.query.delete()
        SavedArticle.query.delete()

        self.client = app.test_client()

        m = Market(code="en-CA", name="United States")

        db.session.add(m)
        db.session.commit()

        self.testuser = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="http://www.picture.com", 
            market="en-CA"
        )

        db.session.add(self.testuser)
        db.session.commit()

    def test_redirect_to_home(self):
        """Test that '/' redirects to '/home'"""

        with self.client as c:
            resp = c.get('/')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 302)
        
    def test_redirect_to_topstories(self):
        """Test that '/home' redirects to '/home/category/topstories'"""

        with self.client as c:
            resp = c.get('/home')

        self.assertEqual(resp.status_code, 302)

    def test_show_category_stories(self):
        """Test that stories are showing on page and are being filtered correctly by category"""
        
        with self.client as c:
            resp = c.get('/home/category/topstories')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Top Stories", html)
    
    def test_show_category_stories_logged_in(self):
        """Test that if a user is logged in, stories are dsplaying correctly from the correct market"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get('/home/category/topstories')
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Canada", html)

    def test_show_search_results(self):
        """Test that a search query will return results"""

        with self.client as c:
            resp = c.get('/search', data={"query": "Sample Search Phrase"})
            html = resp.get_data(as_text=True)

        
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Sample Search Phrase", html)

    def test_save_article(self):
        """Test ability to save articles from homepage"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/article/save', json={"url": "www.test.com", "name": "Fav Article"})

        user_articles = SavedArticle.query.filter_by(user_id=self.testuser.id).all()

        self.assertEqual(len(user_articles), 1)
        self.assertEqual(user_articles[0].name, "Fav Article")

    def test_unsave_article(self):
        """Test ability to unsave articles from homepage"""

        saved_article = SavedArticle(user_id=self.testuser.id, url="www.test.com", name="Fav Article")

        db.session.add(saved_article)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/article/save', json={"url": "www.test.com", "name": "Fav Article"})

        user_articles = SavedArticle.query.filter_by(user_id=self.testuser.id).all()
        self.assertEqual(len(user_articles), 0)





        