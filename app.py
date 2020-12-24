from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Root Route
@app.route("/")
def index():
    marsInfo = mongo.db.marsInfo.find_one()
    return render_template("index.html", marsInfo=marsInfo)

# Scrape Route
@app.route("/scrape")
def scraper():
    marsInfo = mongo.db.marsInfo

    # Run scrape functions and save the data
    marsData = scrape_mars.scrape()
    marsInfo.update({}, marsData, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)