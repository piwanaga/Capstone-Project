import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, connect_db, User, SavedArticle, Market, Category, MarketCategory, STORIES, TOPICS
from forms import RegisterForm, LoginForm, EditUserForm
import requests
from datetime import datetime
from dateutil.parser import parse


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///currant'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = 'CURR_USER_KEY'

URL = 'https://bing-news-search1.p.rapidapi.com/news'
HEADERS = {
            'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
            'x-rapidapi-key': "a80ce0121dmsh365895082cebc39p1be74ajsncac0016effde",
            'x-bingapis-sdk': "true"
        }


@app.template_filter('convert_dt')
def convert_dt_filter(s):
    dt = parse(s)
    return dt.strftime("%b %d %Y %H:%M")

@app.before_request
def add_user_to_g():
    """If logged in, add current user to g variable"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        g.CATEGORIES = MarketCategory.query.filter_by(mkt_code=g.user.market).all()
    
    else:
        g.user = None
        g.CATEGORIES = MarketCategory.query.filter_by(mkt_code="en-US").all()

def do_login(user):
    """Add current user id to session"""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Remove current user id from session"""

    del session[CURR_USER_KEY]

@app.route('/')
def redirect_to_home():
    """Redirect to homepage"""
    
    return redirect('/home')
    

@app.route('/home')
def redirect_to_topstories():
    """Reidrect to '/home/category/topstories""" 

    return redirect('/home/category/topstories')
    
    
"""----------------------ARTICLE ROUTES----------------------"""


@app.route('/home/category/<cat_name>')
def show_category_stories(cat_name):
    """Show top articles for the selected category"""

    stories_querystring = {"mkt":"en-US","safeSearch":"Off","textFormat":"Raw"}

    if g.user:
        stories_querystring["mkt"] = f"{g.user.market}"

    if cat_name != "topstories":
        stories_querystring.update(category = f"{cat_name}")
    
    stories_resp = requests.get(URL, headers=HEADERS, params=stories_querystring)
    stories_json = stories_resp.json()
    stories = stories_json["value"]

    topics_querystring = {"textFormat":"Raw","safeSearch":"Off", "count":"10"}
    topics_resp = requests.get(URL+'/trendingtopics', headers=HEADERS, params=topics_querystring)
    topics_json = topics_resp.json()
    topics = topics_json["value"]
    
    
    if not g.user:
        return render_template('index.html', stories=stories, topics=topics, categories=g.CATEGORIES, cat_name=cat_name)

    saved_article_urls = [article.url for article in g.user.saved_articles]
    return render_template('index.html', stories=stories, topics=topics, categories=g.CATEGORIES, cat_name=cat_name, saved_article_urls=saved_article_urls)

@app.route('/search')
def show_search_results():
    """Return articles related to query"""

    query = request.args.get('q')

    querystring = {"q":f"{query}","freshness":"Day","textFormat":"Raw","safeSearch":"Off"}
    resp = requests.get(URL+'/search', headers=HEADERS, params=querystring)
    resp_json = resp.json()

    stories = resp_json["value"]

    return render_template('search-results.html', query=query, stories=stories, categories=g.CATEGORIES)

@app.route('/article/save', methods=["POST"])
def save_article():
    """Add an article to a user's saved articles list"""
    
    if not g.user:
        return "fail"
        
    else:
        user_id = g.user.id
        url = request.json.get("url")
        name = request.json.get("name")

        saved_articles = g.user.saved_articles
        saved_article_urls = [article.url for article in saved_articles]

        if url in saved_article_urls:
            SavedArticle.query.filter(SavedArticle.user_id==user_id, SavedArticle.url==url).delete()
            db.session.commit()
            return "deleted"

        else:
            saved_article = SavedArticle(user_id=user_id, url=url, name=name)

            g.user.saved_articles.append(saved_article)
            db.session.commit()
            return "success"

@app.route('/article/delete', methods=["POST"])
def remove_article():
    """Remove article from user favorites"""

    if not g.user:
        return "fail"

    else:
        user_id = g.user.id
        url = request.json.get("url")

        SavedArticle.query.filter(SavedArticle.user_id==user_id, SavedArticle.url==url).delete()
        db.session.commit()

        flash("Article removed from favorites", "danger")
        return "success"


"""-------------------------USER ROUTES-------------------------"""


@app.route('/user/register', methods=["GET", "POST"])
def show_register_form():
    """Show registraion form. If form is being submitted, handle form"""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            
            db.session.commit()
            
        except InvalidRequestError:
            db.session.rollback()
            custom_error = "Username/Email already taken"
            return render_template('register-form.html', form=form, custom_error=custom_error)
        except IntegrityError:
            db.session.rollback()
            custom_error = "Username/Email already taken"
            return render_template('register-form.html', form=form, custom_error=custom_error)

        do_login(user)
        flash("Registration successful", "info")
        return redirect('/')

    return render_template('register-form.html', form=form)

@app.route('/user/login', methods=["GET", "POST"])
def show_login_form():
    """Show login form. If form is being submitted, handle form"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome back {user.username}!", "info")
            return redirect('/')
        
        custom_error = "Invalid Username/Password"

        return render_template('login-form.html', form=form, custom_error=custom_error)

    return render_template('login-form.html', form=form)

@app.route('/user/logout')
def logout_user():
    """Logout current user and redirect to homepage"""

    if g.user:
        do_logout()
        flash("Logged out successfully", "info")
        return redirect('/')
    
    return redirect('/')

@app.route('/user/<int:user_id>')
def edit_user(user_id):
    """Show user details"""

    if not g.user:
        flash("Must be logged in to view profile", "danger")
        return redirect('/')

    saved_articles = SavedArticle.query.filter_by(user_id=user_id).all()

    return render_template('user.html', saved_articles=saved_articles)

@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def show_user(user_id):
    """Show form to edit user details"""
    if not g.user:
        flash("Must be logged in to view profile", "danger")
        return redirect('/')

    
    user = User.query.get(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.email=form.email.data,
        user.username=form.username.data,
        user.image_url=form.image_url.data or User.image_url.default.arg
        user.market=form.market.data

        db.session.commit()

        return redirect(f'/user/{user_id}')

    return render_template('user-edit-form.html', form=form)






       
        

    





