from config import mongo_uri
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri=mongo_uri)

@app.route("/")
def index():
    mission = mongo.db.missions.find_one()
    print(f"Mission: {mission}")
    return render_template("index.html", mission=mission)


@app.route("/scrape")
def scraper():
    missions = mongo.db.missions
    mission_data = scrape_mars.scrape()
    missions.update({}, mission_data, upsert=True)
    return redirect("/", code=302)

def default_mission():
    return {
        'news_title': '',
        'news_p': '',
        'featured_image_url': '#',
        'facts_table': '',
        'hemisphere_image_urls': [{'title': '', 'img_url': '#'}]
    }

missions = mongo.db.missions
mission_data = default_mission()
missions.update({}, mission_data, upsert=True)

if __name__ == "__main__":
    app.run(debug=True)