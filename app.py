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

    # Returns Dictionary of Title, Text 
    newFromMars = scrapeMarsNews()
    # Returns Image URL
    spaceImage = scrapeSpaceImages()
    # Returns HTML String of table
    marsFacts = scrapeMarsFacts()
    # Returns list of dictionaries of Title, Image URL
    hemispheres = scrapeMarsHemispheres()