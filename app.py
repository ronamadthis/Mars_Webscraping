from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

mongo = PyMongo(app)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.marsDict
collection = db.marsDict

@app.route('/')
def index():
    marsDict = mongo.db.marsDict.find_one()
    return render_template('index.html', marsDict=marsDict)

@app.route('/scrape')
def scrape():
    marsDict = mongo.db.marsDict
    marsDict_data = scrape_mars.scrape()
    marsDict.update(
        {},
        marsDict_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
