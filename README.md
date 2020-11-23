# Currant News Aggregator
Link to app: https://currant-news.herokuapp.com/

This website displays current news stories using the Bing News Search API. The homepage displays top stories and trending topics, with links to register/login, filter stories by category and search stories by keywords. Users are able to create accounts, which allows them to save articles and set their preferred region from which to pull stories.  

The goal of this website was to sucessfully integrate an external API into an app and build functionality around that. Mainly I wanted to use each of the endpoints offered by this API, which are Categories, Search and Trending Topics. I also wanted to implement authentication and utilize a database to store user data. 

Users can visit the site and immediately view all the top stories across all categories (Categories endpoint) from the Bing News Search API. There is also a list of all the trending topics (Trending Topics endpoint) which can be clicked to return articles about that particular topic. Additionally from the homepage, users can search articles for keywords (Search endpoint), filter the top stories by categories, and click a link to create an account. Once a user has created an account, they are able to click a star icon on each story-card to add that story to their favorites. Once logged in, users can view their own profile, which allows them to view all of their favorited stories as well as edit their own profile, including setting their preferred region (from a list of Bing's supported markets) from which to pull articles. 

Another area of focus for this site was a mobile first design. Using Bootstrap, I wanted the site to be responsive and look good on a small screen first. I accomplished this by using collapsible navigation and hiding/shrinking elements for a small screen. 

The API used can be found here: https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/bing-news-search1/endpoints.
I found this API to be easy to work with and well documented.

Technology Stack:
- HTML
- CSS
- Bootstrap
- JavaScript
- JQuery
- Axios
- Python
- Flask
- SQLAlchemy
- Postgresql
- WTForms




