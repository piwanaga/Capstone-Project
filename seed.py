from app import db
from models import User, SavedArticle, Market, Category, MarketCategory

db.drop_all()
db.create_all()

codes = [
    Market(code="en-AU", name="Australia"),
    Market(code="en-CA", name="Canada"),
    Market(code="zh-CN", name="China"),
    Market(code="en-IN", name="India"),
    Market(code="ja-JP", name="Japan"),
    Market(code="en-GB", name="United Kingdom"),
    Market(code="en-US", name="United States")
        ] 

db.session.bulk_save_objects(codes)
db.session.commit()

categories = [
        Category(name="auto", icon="fas fa-car"),
        Category(name="australia", icon="far fa-flag"),
        Category(name="business", icon="far fa-credit-card"),
        Category(name="canada", icon="far fa-flag"),
        Category(name="china", icon="far fa-flag"),
        Category(name="education", icon="fas fa-graduation-cap"),
        Category(name="entertainment", icon="fas fa-ticket-alt"),
        Category(name="health", icon="fas fa-heartbeat"),
        Category(name="india", icon="far fa-flag"),
        Category(name="japan", icon="far fa-flag"),
        Category(name="lifestyle", icon="fas fa-spa"),
        Category(name="military", icon="fas fa-plane-departure"),
        Category(name="politics", icon="fas fa-landmark"),
        Category(name="products", icon="fas fa-mobile-alt"),
        Category(name="realestate", icon="fas fa-sign"),
        Category(name="scienceandtechnology", icon="fas fa-microscope"),
        Category(name="society", icon="fas fa-user-friends"),
        Category(name="sports", icon="fas fa-football-ball"),
        Category(name="uk", icon="far fa-flag"),
        Category(name="us", icon="far fa-flag"),
        Category(name="world", icon="fas fa-globe"),
        Category(name="topstories", icon="fas fa-home")
        ]

db.session.bulk_save_objects(categories)
db.session.commit()

mkt_categories = [
    MarketCategory(mkt_code="en-AU", cat_name="topstories"),
    MarketCategory(mkt_code="en-AU", cat_name="australia"),
    MarketCategory(mkt_code="en-AU", cat_name="business"),
    MarketCategory(mkt_code="en-AU", cat_name="entertainment"),
    MarketCategory(mkt_code="en-AU", cat_name="politics"),
    MarketCategory(mkt_code="en-AU", cat_name="sports"),
    MarketCategory(mkt_code="en-AU", cat_name="world"),
    MarketCategory(mkt_code="en-CA", cat_name="topstories"),
    MarketCategory(mkt_code="en-CA", cat_name="business"),
    MarketCategory(mkt_code="en-CA", cat_name="canada"),
    MarketCategory(mkt_code="en-CA", cat_name="entertainment"),
    MarketCategory(mkt_code="en-CA", cat_name="lifestyle"),
    MarketCategory(mkt_code="en-CA", cat_name="politics"),
    MarketCategory(mkt_code="en-CA", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="en-CA", cat_name="sports"),
    MarketCategory(mkt_code="en-CA", cat_name="world"),
    MarketCategory(mkt_code="zh-CN", cat_name="topstories"),
    MarketCategory(mkt_code="zh-CN", cat_name="auto"),
    MarketCategory(mkt_code="zh-CN", cat_name="business"),
    MarketCategory(mkt_code="zh-CN", cat_name="china"),
    MarketCategory(mkt_code="zh-CN", cat_name="education"),
    MarketCategory(mkt_code="zh-CN", cat_name="entertainment"),
    MarketCategory(mkt_code="zh-CN", cat_name="military"),
    MarketCategory(mkt_code="zh-CN", cat_name="realestate"),
    MarketCategory(mkt_code="zh-CN", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="zh-CN", cat_name="society"),
    MarketCategory(mkt_code="zh-CN", cat_name="sports"),
    MarketCategory(mkt_code="zh-CN", cat_name="world"),
    MarketCategory(mkt_code="en-IN", cat_name="topstories"),
    MarketCategory(mkt_code="en-IN", cat_name="business"),
    MarketCategory(mkt_code="en-IN", cat_name="entertainment"),
    MarketCategory(mkt_code="en-IN", cat_name="india"),
    MarketCategory(mkt_code="en-IN", cat_name="lifestyle"),
    MarketCategory(mkt_code="en-IN", cat_name="politics"),
    MarketCategory(mkt_code="en-IN", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="en-IN", cat_name="sports"),
    MarketCategory(mkt_code="en-IN", cat_name="world"),
    MarketCategory(mkt_code="ja-JP", cat_name="topstories"),
    MarketCategory(mkt_code="ja-JP", cat_name="business"),
    MarketCategory(mkt_code="ja-JP", cat_name="entertainment"),
    MarketCategory(mkt_code="ja-JP", cat_name="japan"),
    MarketCategory(mkt_code="ja-JP", cat_name="lifestyle"),
    MarketCategory(mkt_code="ja-JP", cat_name="politics"),
    MarketCategory(mkt_code="ja-JP", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="ja-JP", cat_name="sports"),
    MarketCategory(mkt_code="ja-JP", cat_name="world"),
    MarketCategory(mkt_code="en-GB", cat_name="topstories"),
    MarketCategory(mkt_code="en-GB", cat_name="business"),
    MarketCategory(mkt_code="en-GB", cat_name="entertainment"),
    MarketCategory(mkt_code="en-GB", cat_name="health"),
    MarketCategory(mkt_code="en-GB", cat_name="politics"),
    MarketCategory(mkt_code="en-GB", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="en-GB", cat_name="sports"),
    MarketCategory(mkt_code="en-GB", cat_name="uk"),
    MarketCategory(mkt_code="en-GB", cat_name="world"),
    MarketCategory(mkt_code="en-US", cat_name="topstories"),
    MarketCategory(mkt_code="en-US", cat_name="business"),
    MarketCategory(mkt_code="en-US", cat_name="entertainment"),
    MarketCategory(mkt_code="en-US", cat_name="health"),
    MarketCategory(mkt_code="en-US", cat_name="politics"),
    MarketCategory(mkt_code="en-US", cat_name="products"),
    MarketCategory(mkt_code="en-US", cat_name="scienceandtechnology"),
    MarketCategory(mkt_code="en-US", cat_name="sports"),
    MarketCategory(mkt_code="en-US", cat_name="us"),
    MarketCategory(mkt_code="en-US", cat_name="world"),
]

db.session.bulk_save_objects(mkt_categories)
db.session.commit()

testuser = User.signup("test@email.com", "testuser", "password")
db.session.commit()

article1 = SavedArticle(user_id=testuser.id, url="http://www.google.com", name="Sports blah blah blah wins the game")
article2 = SavedArticle(user_id=testuser.id, url="http://www.bing.com", name="Bing is a an alternative to google")

db.session.add_all([article1, article2])
db.session.commit()




