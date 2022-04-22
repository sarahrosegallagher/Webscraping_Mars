
#imports 

from flask import Flask, render_template, redirect, url_for

from flask_pymongo import PyMongo

import scraping

#flask 
app = Flask(__name__)

# connect to mongo via pymongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# --- app routes ---

#home db cxn
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#scrape route 
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)   #update the database using:  .update_one(query_parameter, {"$set": data}, options)

   return redirect('/', code=302) #navigate our page back to / where we can see the updated content.

#run flask
if __name__ == "__main__":
   app.run()  













