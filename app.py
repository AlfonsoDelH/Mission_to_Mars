from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app= Flask(__name__)

conn ="mongodb://localhost:27017"
client=pymongo.MongoClient(conn)
db=client.mars_db
db.mars_info.drop()
db.mars_info.insert_many([scrape_mars.scrape()])

@app.route("/")
def home ():
    mars_website=db.mars_info.find_one()
    return render_template("index.html",information=mars_website)

@app.route("/scrape")
def scrape():
    
    mars_data=scrape_mars.scrape()
    db.mars_info.update({}, mars_data, upsert=True)

    return redirect("/",code=302)

if __name__=="__main__":
    app.run(debug=True)