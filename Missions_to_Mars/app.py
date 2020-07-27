from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mars_latest = mongo.db.mars_latest.find_one()
    return render_template("index.html", mars_latest=mars_latest)


@app.route("/scrape")
def scraper():
    mars_latest = mongo.db.mars_latest
    mars_latest_data = scrape_mars.scrape()
    mars_latest.update({}, mars_latest_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
